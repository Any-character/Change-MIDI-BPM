# MIDI BPM Changer / MIDI BPM 更改工具

Change MIDI BPM while keeping the actual duration unchanged.

更改 MIDI 文件的 BPM，同时保持实际时长完全不变。

---

## Features / 功能

- **Keep Duration / 保持时长**: Change BPM without changing how the music sounds.
- **Quantize / 量化**: Quantize notes to a customizable grid (1/4, 1/8, 1/16, 1/32).
- **Trim Silence / 裁剪开头空白**: Remove leading silence so the first note starts at tick 0.
- **Audio BPM Detection / 音频 BPM 检测**: Detect BPM from audio files (MP3, WAV, FLAC, M4A, etc.).
- **Bilingual UI / 双语界面**: Chinese and English.

---

## Installation / 安装

```bash
pip install -r requirements.txt
```

---

## Usage / 使用

### GUI / 图形界面

Windows:
```bash
start.bat
```

Or run directly: / 或直接运行：
```bash
python change_midi_bpm_gui.py
```

### CLI / 命令行

```bash
python change_midi_bpm.py <input.mid> <target_bpm> [--trim] [--quantize N]
```

Example / 示例：
```bash
python change_midi_bpm.py input.mid 140 --trim --quantize 16
```

---

## How It Works / 工作原理

Standard MIDI editors change BPM by keeping tick counts the same, which changes the actual duration. This tool scales all event ticks proportionally so that the actual duration stays exactly the same while only the BPM value changes.

普通 MIDI 编辑软件改 BPM 后音符 tick 数不变，导致实际时长变化。本工具将所有事件的 tick 值按 BPM 比例缩放，使实际时长完全不变，仅 BPM 数值改变。

---

## License / 许可证

MIT License
