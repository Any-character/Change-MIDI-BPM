import sys
import os
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

try:
    import mido
except ImportError:
    print("错误：缺少 mido 库，请先运行：pip install mido")
    sys.exit(1)

librosa_available = False
try:
    import librosa
    librosa_available = True
except ImportError:
    pass


LANG = {
    'zh': {
        'title': 'MIDI BPM 更改工具（保持时长不变）',
        'select_file': '选择 MIDI 文件',
        'browse': '浏览...',
        'bpm_settings': 'BPM 设置',
        'original_bpm': '原始 BPM：',
        'target_bpm': '目标 BPM：',
        'detect_from_audio': '从音频检测',
        'trim': '裁剪开头空白（使第一个音符前无空白）',
        'quantize': '量化音符',
        'quantize_granularity': '颗粒度:',
        'quantize_note': '(1/n 音符)',
        'convert': '开始转换',
        'log': '处理日志',
        'loaded_file': '已加载文件:',
        'original_bpm_val': '原始 BPM:',
        'analyzing_bpm': '从音频检测 BPM:',
        'detected_bpm': '检测到的 BPM 值：',
        'bpm_set_to': '已将目标 BPM 设置为:',
        'cannot_detect_bpm': '无法从音频文件检测出 BPM',
        'bpm_detection_note': '⚠ 注意：音频 BPM 检测可能存在 ±1-2 BPM 的误差',
        'bpm_detection_note2': '      如果检测结果不准确，请手动调整目标 BPM',
        'please_select_file': '请先选择 MIDI 文件',
        'file_not_found': '文件不存在',
        'target_bpm_must_be_number': '目标 BPM 必须是数字',
        'target_bpm_must_be_positive': '目标 BPM 必须大于 0',
        'quantize_must_be_number': '量化颗粒度必须是数字',
        'start_convert': '开始转换...',
        'convert_complete': '转换完成！',
        'success': '成功',
        'output_file': '输出文件：',
        'error': '错误',
        'convert_failed': '转换失败：',
        'read_file_failed': '读取文件失败：',
        'librosa_not_installed': '未安装 librosa 库，请运行：pip install librosa',
        'original_bpm_label': '原始 BPM:',
        'target_bpm_label': '目标 BPM:',
        'scale_factor': '时间缩放比例:',
        'tempo_added': '已添加 tempo 事件: BPM=',
        'quantize_level': '量化颗粒度: 1/{0} 音符 ({1} ticks)',
        'quantize_complete': '量化完成',
        'trim_duration': '裁剪开头空白: {0} ticks ({1:.3f} 秒)',
        'trim_complete': '裁剪完成',
        'no_blank_to_trim': '无开头空白需要裁剪',
        'saved_to': '已保存到:',
        'verification': '验证：',
        'original_duration': '原文件实际时长:',
        'new_duration': '新文件实际时长:',
        'quantize_duration_note': '⚠ 注意：量化会使时长产生微小变化',
        'trim_duration_label': '裁剪开头空白时长:',
        'expected_duration': '预期时长（原时长 - 裁剪时长）:',
        'actual_diff': '实际差异:',
        'duration_diff': '时长差异:',
        'quantize_duration_change': '量化导致的时长变化:',
        'language': '语言',
    },
    'en': {
        'title': 'MIDI BPM Changer (Keep Duration)',
        'select_file': 'Select MIDI File',
        'browse': 'Browse...',
        'bpm_settings': 'BPM Settings',
        'original_bpm': 'Original BPM:',
        'target_bpm': 'Target BPM:',
        'detect_from_audio': 'Detect from Audio',
        'trim': 'Trim leading silence (no silence before first note)',
        'quantize': 'Quantize Notes',
        'quantize_granularity': 'Granularity:',
        'quantize_note': '(1/n note)',
        'convert': 'Start Conversion',
        'log': 'Process Log',
        'loaded_file': 'Loaded file:',
        'original_bpm_val': 'Original BPM:',
        'analyzing_bpm': 'Detecting BPM from audio:',
        'detected_bpm': 'Detected BPM values:',
        'bpm_set_to': 'Target BPM set to:',
        'cannot_detect_bpm': 'Cannot detect BPM from audio file',
        'bpm_detection_note': '⚠ Note: Audio BPM detection may have ±1-2 BPM error',
        'bpm_detection_note2': '      If result is inaccurate, manually adjust target BPM',
        'please_select_file': 'Please select a MIDI file first',
        'file_not_found': 'File does not exist',
        'target_bpm_must_be_number': 'Target BPM must be a number',
        'target_bpm_must_be_positive': 'Target BPM must be greater than 0',
        'quantize_must_be_number': 'Quantize granularity must be a number',
        'start_convert': 'Starting conversion...',
        'convert_complete': 'Conversion complete!',
        'success': 'Success',
        'output_file': 'Output file:',
        'error': 'Error',
        'convert_failed': 'Conversion failed:',
        'read_file_failed': 'Failed to read file:',
        'librosa_not_installed': 'librosa library not installed, please run: pip install librosa',
        'original_bpm_label': 'Original BPM:',
        'target_bpm_label': 'Target BPM:',
        'scale_factor': 'Time scale factor:',
        'tempo_added': 'Added tempo event: BPM=',
        'quantize_level': 'Quantize level: 1/{0} note ({1} ticks)',
        'quantize_complete': 'Quantization complete',
        'trim_duration': 'Trimming leading silence: {0} ticks ({1:.3f} seconds)',
        'trim_complete': 'Trimming complete',
        'no_blank_to_trim': 'No leading silence to trim',
        'saved_to': 'Saved to:',
        'verification': 'Verification:',
        'original_duration': 'Original duration:',
        'new_duration': 'New duration:',
        'quantize_duration_note': '⚠ Note: Quantization may slightly change duration',
        'trim_duration_label': 'Trimmed silence duration:',
        'expected_duration': 'Expected duration (original - trimmed):',
        'actual_diff': 'Actual difference:',
        'duration_diff': 'Duration difference:',
        'quantize_duration_change': 'Duration change from quantization:',
        'language': 'Language',
    }
}

current_lang = 'zh'


def get_tempo_from_midi(midi_file):
    mid = mido.MidiFile(midi_file)
    for track in mid.tracks:
        for msg in track:
            if msg.type == 'set_tempo':
                tempo = msg.tempo
                bpm = mido.tempo2bpm(tempo)
                return bpm
    return 120.0


def detect_audio_bpm(audio_file):
    """从音频文件检测BPM（使用librosa）"""
    if not librosa_available:
        return None
    
    try:
        y, sr = librosa.load(audio_file, sr=None, mono=True)
        
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        
        if isinstance(tempo, (list, tuple)):
            tempo = tempo[0]
        elif hasattr(tempo, '__len__') and len(tempo) > 0:
            tempo = tempo[0]
        
        candidates = [round(float(tempo))]
        
        if tempo < 60:
            candidates.append(round(tempo * 2))
        elif tempo > 180:
            candidates.append(round(tempo / 2))
        
        candidates = sorted(set(candidates))
        
        return candidates
    except Exception as e:
        print(f"检测BPM错误: {e}")
        return None


def quantize_midi(mid, grid_value, log_func=None):
    """
    量化MIDI音符到指定网格
    
    grid_value: 量化颗粒度（分母），如 4=四分音符, 8=八分音符, 16=十六分音符
    """
    def log(msg):
        if log_func:
            log_func(msg)
        else:
            print(msg)
    
    grid_size = mid.ticks_per_beat * 4 // grid_value
    log(LANG[current_lang]['quantize_level'].format(grid_value, grid_size))
    
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
    
    log(LANG[current_lang]['quantize_complete'])


def change_bpm_keep_duration(input_path, output_path, target_bpm, trim=False, quantize=0, log_func=None):
    def log(msg):
        if log_func:
            log_func(msg)
        else:
            print(msg)

    mid = mido.MidiFile(input_path)

    original_bpm = get_tempo_from_midi(input_path)
    log(LANG[current_lang]['original_bpm_label'] + f" {original_bpm:.2f}")
    log(LANG[current_lang]['target_bpm_label'] + f" {target_bpm:.2f}")

    scale_factor = target_bpm / original_bpm
    log(LANG[current_lang]['scale_factor'] + f" {scale_factor:.4f}")

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
            if j == 0:
                new_msg.time = abs_tick
            else:
                new_msg.time = abs_tick - events[j-1][0]

            if new_msg.type == 'set_tempo':
                new_tempo = mido.bpm2tempo(target_bpm)
                new_msg.tempo = new_tempo
                tempo_added = True

            new_track.append(new_msg)

        if not has_tempo and not tempo_added and i == 1 and len(track) > 0:
            new_track.insert(0, mido.MetaMessage('set_tempo', tempo=mido.bpm2tempo(target_bpm), time=0))
            tempo_added = True
            log(LANG[current_lang]['tempo_added'] + f"{target_bpm:.2f}")

        new_mid.tracks.append(new_track)

    if quantize > 0:
        quantize_midi(new_mid, quantize, log_func=log)

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
            log(LANG[current_lang]['trim_duration'].format(first_note_tick, trim_duration))
            for track in new_mid.tracks:
                abs_tick = 0
                prev_new_abs = 0
                for msg in track:
                    abs_tick += msg.time
                    new_abs = max(0, abs_tick - first_note_tick)
                    msg.time = new_abs - prev_new_abs
                    prev_new_abs = new_abs
            log(LANG[current_lang]['trim_complete'])
        else:
            log(LANG[current_lang]['no_blank_to_trim'])

    new_mid.save(output_path)
    log(LANG[current_lang]['saved_to'] + f" {output_path}")

    actual_duration_original = mid.length
    actual_duration_new = new_mid.length
    log("")
    log(LANG[current_lang]['verification'])
    log(f"  {LANG[current_lang]['original_duration']} {actual_duration_original:.3f} " + ('秒' if current_lang == 'zh' else 'seconds'))
    log(f"  {LANG[current_lang]['new_duration']} {actual_duration_new:.3f} " + ('秒' if current_lang == 'zh' else 'seconds'))
    
    if quantize > 0:
        log(f"  {LANG[current_lang]['quantize_duration_note']}")
    
    if trim_duration > 0:
        expected_duration = actual_duration_original - trim_duration
        diff_after_trim = abs(actual_duration_new - expected_duration)
        log(f"  {LANG[current_lang]['trim_duration_label']} {trim_duration:.3f} " + ('秒' if current_lang == 'zh' else 'seconds'))
        log(f"  {LANG[current_lang]['expected_duration']} {expected_duration:.3f} " + ('秒' if current_lang == 'zh' else 'seconds'))
        log(f"  {LANG[current_lang]['actual_diff']} {diff_after_trim:.6f} " + ('秒' if current_lang == 'zh' else 'seconds'))
    else:
        diff = abs(actual_duration_new - actual_duration_original)
        log(f"  {LANG[current_lang]['duration_diff']} {diff:.6f} " + ('秒' if current_lang == 'zh' else 'seconds'))
        if quantize > 0:
            log(f"  {LANG[current_lang]['quantize_duration_change']} {diff:.6f} " + ('秒' if current_lang == 'zh' else 'seconds'))

    return original_bpm, actual_duration_original, actual_duration_new


class MidiBpmApp:
    def __init__(self, root):
        global current_lang

        # 加载配置文件
        config_path = os.path.join(os.path.dirname(__file__), 'config.txt')
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line.startswith('language='):
                            lang = line.split('=', 1)[1].strip()
                            if lang in LANG:
                                current_lang = lang
            except Exception:
                pass

        self.root = root
        self.root.title(LANG[current_lang]['title'])
        self.root.geometry("600x560")
        self.root.resizable(False, False)

        self.input_path = tk.StringVar()
        self.target_bpm = tk.StringVar(value="120")
        self.original_bpm_str = tk.StringVar(value="--")
        self.trim_var = tk.BooleanVar(value=False)
        self.quantize_var = tk.BooleanVar(value=False)
        self.quantize_value = tk.StringVar(value="16")

        self._build_ui()

    def _build_ui(self):
        pad = {"padx": 12, "pady": 6}

        frm_lang = tk.Frame(self.root)
        frm_lang.pack(fill="x", padx=12, pady=4)
        tk.Label(frm_lang, text=LANG[current_lang]['language']).pack(side="left")
        lang_options = [('中文', 'zh'), ('English', 'en')]
        self.lang_var = tk.StringVar(value=current_lang)
        lang_menu = tk.OptionMenu(frm_lang, self.lang_var, *[l[1] for l in lang_options], command=self.change_language)
        lang_menu.config(width=10)
        lang_menu.pack(side="left", padx=4)

        frm_file = tk.LabelFrame(self.root, text=LANG[current_lang]['select_file'])
        frm_file.pack(fill="x", **pad)

        tk.Entry(frm_file, textvariable=self.input_path).pack(
            side="left", fill="x", expand=True, padx=8, pady=8
        )
        tk.Button(frm_file, text=LANG[current_lang]['browse'], command=self.choose_file, width=12).pack(
            side="right", padx=8, pady=8
        )

        frm_bpm = tk.LabelFrame(self.root, text=LANG[current_lang]['bpm_settings'])
        frm_bpm.pack(fill="x", **pad)

        tk.Label(frm_bpm, text=LANG[current_lang]['original_bpm']).grid(row=0, column=0, sticky="e", padx=8, pady=6)
        tk.Label(frm_bpm, textvariable=self.original_bpm_str, fg="blue", width=10, anchor="w").grid(
            row=0, column=1, sticky="w"
        )

        tk.Label(frm_bpm, text=LANG[current_lang]['target_bpm']).grid(row=1, column=0, sticky="e", padx=8, pady=6)
        tk.Entry(frm_bpm, textvariable=self.target_bpm, width=12).grid(
            row=1, column=1, sticky="w"
        )
        tk.Button(frm_bpm, text=LANG[current_lang]['detect_from_audio'], command=self.detect_audio_bpm_ui, width=16).grid(
            row=1, column=2, sticky="w", padx=4
        )

        tk.Checkbutton(
            frm_bpm, text=LANG[current_lang]['trim'], variable=self.trim_var
        ).grid(row=2, column=0, columnspan=3, sticky="w", padx=8, pady=6)

        frm_quantize = tk.Frame(frm_bpm)
        frm_quantize.grid(row=3, column=0, columnspan=3, sticky="w", padx=8, pady=6)
        tk.Checkbutton(
            frm_quantize, text=LANG[current_lang]['quantize'], variable=self.quantize_var
        ).pack(side="left")
        tk.Label(frm_quantize, text=LANG[current_lang]['quantize_granularity']).pack(side="left", padx=4)
        quantize_options = ["4", "8", "16", "32"]
        tk.OptionMenu(frm_quantize, self.quantize_value, *quantize_options).pack(side="left", padx=2)
        tk.Label(frm_quantize, text=LANG[current_lang]['quantize_note'], fg="gray").pack(side="left", padx=2)

        tk.Button(
            self.root, text=LANG[current_lang]['convert'], command=self.convert, height=2, bg="#4CAF50", fg="white"
        ).pack(fill="x", padx=12, pady=4)

        frm_log = tk.LabelFrame(self.root, text=LANG[current_lang]['log'])
        frm_log.pack(fill="both", expand=True, **pad)

        self.log_text = scrolledtext.ScrolledText(frm_log, height=16, state="disabled")
        self.log_text.pack(fill="both", expand=True, padx=8, pady=8)

    def change_language(self, lang_code):
        global current_lang
        current_lang = lang_code

        # 保存语言设置到配置文件
        config_path = os.path.join(os.path.dirname(__file__), 'config.txt')
        try:
            with open(config_path, 'w', encoding='utf-8') as f:
                f.write(f'language={lang_code}\n')
        except Exception:
            pass

        # 保存当前用户数据
        saved_input = self.input_path.get()
        saved_target_bpm = self.target_bpm.get()
        saved_original_bpm = self.original_bpm_str.get()
        saved_trim = self.trim_var.get()
        saved_quantize = self.quantize_var.get()
        saved_quantize_value = self.quantize_value.get()

        # 销毁所有子组件
        for widget in self.root.winfo_children():
            widget.destroy()

        # 重新构建 UI
        self._build_ui()

        # 恢复用户数据
        self.input_path.set(saved_input)
        self.target_bpm.set(saved_target_bpm)
        self.original_bpm_str.set(saved_original_bpm)
        self.trim_var.set(saved_trim)
        self.quantize_var.set(saved_quantize)
        self.quantize_value.set(saved_quantize_value)

        # 更新语言选择器的值
        self.lang_var.set(lang_code)
        self.root.title(LANG[current_lang]['title'])

        messagebox.showinfo(LANG[current_lang]['success'],
                           LANG[current_lang]['language'] + ' ' +
                           ('已更改为中文' if lang_code == 'zh' else 'changed to English'))

    def _log(self, msg):
        self.log_text.config(state="normal")
        self.log_text.insert("end", msg + "\n")
        self.log_text.see("end")
        self.log_text.config(state="disabled")
        self.root.update_idletasks()

    def choose_file(self):
        path = filedialog.askopenfilename(
            title=LANG[current_lang]['select_file'],
            filetypes=[("MIDI 文件", "*.mid *.midi"), ("所有文件", "*.*")],
        )
        if path:
            self.input_path.set(path)
            try:
                bpm = get_tempo_from_midi(path)
                self.original_bpm_str.set(f"{bpm:.2f}")
                self.target_bpm.set(f"{bpm:.0f}")
                self._log(LANG[current_lang]['loaded_file'] + f" {path}")
                self._log(LANG[current_lang]['original_bpm_val'] + f" {bpm:.2f}")
            except Exception as e:
                messagebox.showerror(LANG[current_lang]['error'], LANG[current_lang]['read_file_failed'] + f" {e}")

    def detect_audio_bpm_ui(self):
        if not librosa_available:
            messagebox.showwarning(LANG[current_lang]['success'], LANG[current_lang]['librosa_not_installed'])
            return

        path = filedialog.askopenfilename(
            title=LANG[current_lang]['select_file'],
            filetypes=[
                ("音频文件", "*.mp3 *.wav *.flac *.m4a *.ogg *.aac"),
                ("所有文件", "*.*"),
            ],
        )
        if not path:
            return

        self._log("")
        self._log("=" * 40)
        self._log(LANG[current_lang]['analyzing_bpm'] + f" {os.path.basename(path)}")

        try:
            bpms = detect_audio_bpm(path)
            if bpms:
                self._log(LANG[current_lang]['detected_bpm'])
                for bpm in bpms:
                    self._log(f"  - BPM = {bpm:.2f}")
                best_bpm = round(bpms[0])
                self.target_bpm.set(f"{best_bpm}")
                self._log(LANG[current_lang]['bpm_set_to'] + f" {best_bpm}")
                self._log("")
                self._log(LANG[current_lang]['bpm_detection_note'])
                self._log(LANG[current_lang]['bpm_detection_note2'])
            else:
                self._log(LANG[current_lang]['cannot_detect_bpm'])
                messagebox.showinfo(LANG[current_lang]['success'], LANG[current_lang]['cannot_detect_bpm'])
        except Exception as e:
            self._log(LANG[current_lang]['error'] + f" {e}")
            messagebox.showerror(LANG[current_lang]['error'], LANG[current_lang]['convert_failed'] + f" {e}")

    def convert(self):
        input_path = self.input_path.get().strip()
        if not input_path:
            messagebox.showwarning(LANG[current_lang]['success'], LANG[current_lang]['please_select_file'])
            return
        if not os.path.exists(input_path):
            messagebox.showerror(LANG[current_lang]['error'], LANG[current_lang]['file_not_found'])
            return

        try:
            target_bpm = float(self.target_bpm.get())
        except ValueError:
            messagebox.showerror(LANG[current_lang]['error'], LANG[current_lang]['target_bpm_must_be_number'])
            return

        if target_bpm <= 0:
            messagebox.showerror(LANG[current_lang]['error'], LANG[current_lang]['target_bpm_must_be_positive'])
            return

        base, ext = os.path.splitext(input_path)
        output_path = f"{base}_bpm{int(target_bpm)}{ext}"

        quantize_value = 0
        if self.quantize_var.get():
            try:
                quantize_value = int(self.quantize_value.get())
            except ValueError:
                messagebox.showerror(LANG[current_lang]['error'], LANG[current_lang]['quantize_must_be_number'])
                return

        self._log("")
        self._log("=" * 40)
        self._log(LANG[current_lang]['start_convert'])

        try:
            change_bpm_keep_duration(input_path, output_path, target_bpm, trim=self.trim_var.get(), quantize=quantize_value, log_func=self._log)
            self._log("")
            self._log(LANG[current_lang]['convert_complete'])
            messagebox.showinfo(LANG[current_lang]['success'], LANG[current_lang]['convert_complete'] + "\n" + LANG[current_lang]['output_file'] + f" {output_path}")
        except Exception as e:
            self._log(LANG[current_lang]['error'] + f" {e}")
            messagebox.showerror(LANG[current_lang]['error'], LANG[current_lang]['convert_failed'] + f" {e}")


def main():
    root = None
    try:
        root = tk.Tk()
        root.withdraw()
        app = MidiBpmApp(root)
        root.deiconify()
        root.mainloop()
    except Exception as e:
        import traceback
        err_msg = traceback.format_exc()
        print("程序启动失败：")
        print(err_msg)
        try:
            if root:
                messagebox.showerror("启动失败", err_msg)
            else:
                tk.Tk().withdraw()
                messagebox.showerror("启动失败", err_msg)
        except:
            pass
        try:
            input("\n按回车键退出...")
        except:
            pass


if __name__ == "__main__":
    main()
