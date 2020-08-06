Dim taskName, strArgs_deleteTask
Const Overwrite = True
Set objShell = CreateObject("WScript.Shell")

'El nombre de la tarea que eliminaremos
taskName = "youtube_test"

'Comando para eliminar la tarea
strArgs_deleteTask = "schtasks /delete /tn " & taskName & " /F"
objShell.Run strArgs_deleteTask, 0, false
set objShell = Nothing