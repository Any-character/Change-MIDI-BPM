Set WshShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")
strDir = fso.GetParentFolderName(WScript.ScriptFullName)
WshShell.CurrentDirectory = strDir

' Check if python is available
Set objExec = WshShell.Exec("python --version")
Do While objExec.Status = 0
    WScript.Sleep 100
Loop

If objExec.ExitCode <> 0 Then
    MsgBox "Python not found. Please install Python 3.x first.", 16, "Error"
    WScript.Quit 1
End If

' Check if mido is installed
Set objExec2 = WshShell.Exec("python -c ""import mido""")
Do While objExec2.Status = 0
    WScript.Sleep 100
Loop

If objExec2.ExitCode <> 0 Then
    result = MsgBox("Installing mido library. Click OK to continue.", 64, "Setup")
    Set objExec3 = WshShell.Exec("pip install mido")
    Do While objExec3.Status = 0
        WScript.Sleep 500
    Loop
    If objExec3.ExitCode <> 0 Then
        MsgBox "Failed to install mido.", 16, "Error"
        WScript.Quit 1
    End If
End If

' Launch GUI (no console window)
WshShell.Run "pythonw change_midi_bpm_gui.py", 0, False
