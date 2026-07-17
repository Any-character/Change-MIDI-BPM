Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "pythonw change_midi_bpm_gui.py", 0, False
Set WshShell = Nothing
