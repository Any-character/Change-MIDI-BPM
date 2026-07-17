#!/usr/bin/env python3
"""MIDI BPM Changer - Change BPM while keeping actual duration unchanged."""

import sys
import os

try:
    import mido
except ImportError:
    print("Error: mido library missing. Run: pip install mido")
    sys.exit(1)


def get_tempo_from_midi(midi_file):
    """Get BPM from the first tempo event in the MIDI file."""
    mid = mido.MidiFile(midi_file)
    for track in mid.tracks:
        for msg in track:
            if msg.type == 'set_tempo':
                return mido.tempo2bpm(msg.tempo)
    return 120.0


def quantize_midi(mid, grid_value):
    """Quantize MIDI events to a grid."""
    grid_size = mid.ticks_per_beat * 4 // grid_value
    print(f"Quantize level: 1/{grid_value} note ({grid_size} ticks)")

    for track in mid.tracks:
        events = []
        abs_tick = 0
        for msg in track:
            abs_tick += msg.time
            quantized_tick = round(abs_tick / grid_size) * grid_size
            events.append((quantized_tick, msg))

        events.sort(key=lambda x: x[0])

        track[:] = []
        prev_tick = 0
        for quantized_tick, msg in events:
            delta = quantized_tick - prev_tick
            new_msg = msg.copy()
            new_msg.time = delta
            track.append(new_msg)
            prev_tick = quantized_tick

    print("Quantization complete")


def change_bpm_keep_duration(input_path, output_path, target_bpm, trim=False, quantize=0):
    """Change MIDI BPM while keeping actual duration unchanged."""
    mid = mido.MidiFile(input_path)

    original_bpm = get_tempo_from_midi(input_path)
    print(f"Original BPM: {original_bpm:.2f}")
    print(f"Target BPM: {target_bpm:.2f}")

    scale_factor = target_bpm / original_bpm
    print(f"Scale factor: {scale_factor:.4f}")

    has_tempo = False
    for track in mid.tracks:
        for msg in track:
            if msg.type == 'set_tempo':
                has_tempo = True
                break
        if has_tempo:
            break

    new_mid = mido.MidiFile()
    new_mid.ticks_per_beat = mid.ticks_per_beat

    tempo_added = False
    for i, track in enumerate(mid.tracks):
        new_track = mido.MidiTrack()

        events = []
        abs_tick = 0
        for msg in track:
            abs_tick += msg.time
            new_abs_tick = round(abs_tick * scale_factor)
            events.append((new_abs_tick, msg))

        for j, (abs_tick, msg) in enumerate(events):
            new_msg = msg.copy()
            new_msg.time = abs_tick if j == 0 else abs_tick - events[j - 1][0]

            if new_msg.type == 'set_tempo':
                new_msg.tempo = mido.bpm2tempo(target_bpm)
                tempo_added = True

            new_track.append(new_msg)

        if not has_tempo and not tempo_added and i == 1 and len(track) > 0:
            new_track.insert(0, mido.MetaMessage('set_tempo', tempo=mido.bpm2tempo(target_bpm), time=0))
            tempo_added = True
            print(f"Added tempo event: BPM={target_bpm:.2f}")

        new_mid.tracks.append(new_track)

    if quantize > 0:
        quantize_midi(new_mid, quantize)

    trim_duration = 0.0
    if trim:
        first_note_tick = None
        for track in new_mid.tracks:
            abs_tick = 0
            for msg in track:
                abs_tick += msg.time
                if msg.type == 'note_on' and msg.velocity > 0:
                    if first_note_tick is None or abs_tick < first_note_tick:
                        first_note_tick = abs_tick
                    break

        if first_note_tick is not None and first_note_tick > 0:
            current_tempo = mido.bpm2tempo(target_bpm)
            trim_duration = (first_note_tick * current_tempo) / (new_mid.ticks_per_beat * 1_000_000)
            print(f"Trimming leading silence: {first_note_tick} ticks ({trim_duration:.3f} seconds)")
            for track in new_mid.tracks:
                abs_tick = 0
                prev_new_abs = 0
                for msg in track:
                    abs_tick += msg.time
                    new_abs = max(0, abs_tick - first_note_tick)
                    msg.time = new_abs - prev_new_abs
                    prev_new_abs = new_abs
            print("Trimming complete")
        else:
            print("No leading silence to trim")

    new_mid.save(output_path)
    print(f"Saved to: {output_path}")

    actual_duration_original = mid.length
    actual_duration_new = new_mid.length
    print()
    print("Verification:")
    print(f"  Original duration: {actual_duration_original:.3f} seconds")
    print(f"  New duration: {actual_duration_new:.3f} seconds")

    if quantize > 0:
        print("  Note: Quantization may slightly change duration")

    if trim_duration > 0:
        expected_duration = actual_duration_original - trim_duration
        diff_after_trim = abs(actual_duration_new - expected_duration)
        print(f"  Trimmed silence: {trim_duration:.3f} seconds")
        print(f"  Expected duration (original - trimmed): {expected_duration:.3f} seconds")
        print(f"  Actual difference: {diff_after_trim:.6f} seconds")
    else:
        diff = abs(actual_duration_new - actual_duration_original)
        print(f"  Duration difference: {diff:.6f} seconds")
        if quantize > 0:
            print(f"  Duration change from quantization: {diff:.6f} seconds")


def main():
    if len(sys.argv) < 3:
        print("Usage: python change_midi_bpm.py <input.mid> <target_bpm> [output.mid] [--trim] [--quantize N]")
        print()
        print("Options:")
        print("  --trim         Remove leading silence")
        print("  --quantize N   Quantize to 1/N note grid (4, 8, 16, 32)")
        print()
        print("Examples:")
        print("  python change_midi_bpm.py input.mid 140")
        print("  python change_midi_bpm.py input.mid 140 output.mid")
        print("  python change_midi_bpm.py input.mid 140 --trim --quantize 16")
        sys.exit(1)

    args = sys.argv[1:]

    trim = '--trim' in args
    if '--trim' in args:
        args.remove('--trim')

    quantize = 0
    for i, arg in enumerate(args):
        if arg == '--quantize' and i + 1 < len(args):
            try:
                quantize = int(args[i + 1])
                args = args[:i] + args[i + 2:]
            except ValueError:
                print("Error: --quantize value must be an integer")
                sys.exit(1)
            break

    if len(args) < 2:
        print("Error: input file and target BPM required")
        sys.exit(1)

    input_path = args[0]

    if not os.path.exists(input_path):
        print(f"Error: file not found: {input_path}")
        sys.exit(1)

    try:
        target_bpm = float(args[1])
    except ValueError:
        print(f"Error: target BPM must be a number: {args[1]}")
        sys.exit(1)

    if target_bpm <= 0:
        print("Error: target BPM must be greater than 0")
        sys.exit(1)

    output_path = args[2] if len(args) >= 3 else f"{os.path.splitext(input_path)[0]}_bpm{int(target_bpm)}.mid"

    change_bpm_keep_duration(input_path, output_path, target_bpm, trim=trim, quantize=quantize)


if __name__ == '__main__':
    main()
