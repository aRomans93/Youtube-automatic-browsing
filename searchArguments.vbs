Dim pythonFileName, argHomeDir, objFSO, strPath, cCurPath, sCurPath, getPython, ObjExec, pythonPath, batFileName, pyPath, batPath
Set objShell = WScript.CreateObject("WScript.Shell")
Dim arrSearch, arrVideo, arrComments, maxInd, minInd, randInt, randInt2, argSearch, argVideo, argComment, pyArgs

'El nombre de nuestro script de python
pythonFileName = "youtube_test.py"
'Los argumentos que recibe nuestro script de python
'Para ingresar nuestros argumentos, es importante que escapemos caracteres especiales para vbs y bat.
'Para escapar un caracter solo hay que repetirlo, por ejemplo, empresa 100% mexicana, seria empresa 100%% mexicana.
'algunos caracteres especiales comunes son: ", %, &, <, >, |, ^

'Lista de valores para el argumento de busqueda
arrSearch = Array(  "seguritech", _
		    "seguridad mexico")
'Lista de valores para el argumento del nombre del video
arrVideo = Array(  "Seguritech, empresa 100%% mexicana que ofrece servicios de seguridad", _
		   "La estrategia de seguridad en México - Agenda Pública")

'Listas de valores para el argumento de comentario
arrComments = Array( 	Array(  "siempre brindando las mejores oportunidades", _
			      	"totalmente de acuerdo con los comentarios anteriores", _
			      	"realmente sorprendente"), _ 
			Array(	"Muy bien", _
			      	"El futuro", _
			      	"Esta es la cuarta transformación")) 

maxInd = UBound(arrSearch)
minInd = LBound(arrSearch)
Randomize
randInt = Int( ( maxInd - minInd + 1 ) * Rnd + minInd )
argSearch = arrSearch(randInt)
argVideo = arrVideo(randInt)
maxInd = UBound(arrComments(randInt))
minInd = LBound(arrComments(randInt))
randInt2 = Int( ( maxInd - minInd + 1 ) * Rnd + minInd )
argComment = arrComments(randInt)(randInt2)

'Pasamos la ruta hacia el perfil del usuario desde aqui como argumento, esta ruta es utilizada dentro del script
argHomeDir = objShell.ExpandEnvironmentStrings("%UserProfile%")

'Obtenemos la ruta de nuestra carpeta
strPath = Wscript.ScriptFullName
Set objFSO = CreateObject("Scripting.FileSystemObject")
Set objFile = objFSO.GetFile(strPath)
cCurPath = objFSO.GetParentFolderName(objFile) 
sCurPath = cCurPath & "\"

'Definimos un comando para obtener la ruta de python.exe y lo ejecutamos
getPython= "python -c ""import sys; print(sys.executable)"""
Set ObjExec = objShell.Exec(getPython)
'Leemos el resultado
Do
    pythonPath = ObjExec.StdOut.ReadLine()
Loop While Not ObjExec.Stdout.atEndOfStream

'Definimos el nombre del archivo bat y lo creamos
batFileName = "run_youtube.bat"
Const ForWriting = 2
Const OpenAsUSAscii =  0  ' Opens the file as ASCII.
batPath = sCurPath & batFileName
'Open write stream
Set objTextFile = objFSO.OpenTextFile(batPath, ForWriting, True, OpenAsUSAscii)

'Escribimos lo que va en el archivo bat
pyPath = sCurPath & pythonFileName
pyArgs = """" & pythonPath & """ """ & pyPath & """ """ &  argSearch & """ """ & argVideo & """ """ & argComment & _
	 """ """ & argHomeDir & """ """ & cCurPath & """"
objTextFile.WriteLine "@echo off"
objTextFile.WriteLine "for /f ""tokens=2 delims=:."" %%x in ('chcp') do set cp=%%x"
objTextFile.WriteLine "chcp 1252>nul"
objTextFile.WriteLine pyArgs
objTextFile.WriteLine "chcp %cp%>nul"
'Close write stream
objTextFile.Close

'Convertimos el formato del archivo bat de utf-8 a ANSI para poder usar palabras acentuadas
Private Const adReadAll = -1
Private Const adSaveCreateOverWrite = 2
Private Const adTypeBinary = 1
Private Const adTypeText = 2
Private Const adWriteChar = 0
Dim strText

With CreateObject("ADODB.Stream")
  .Open
  .Type = adTypeBinary
  .LoadFromFile batPath
  .Type = adTypeText
  .Charset = "utf-8"
  strText = .ReadText(adReadAll)
  .Position = 0
  .SetEOS
  .Charset = "iso-8859-1"
  .WriteText strText, adWriteChar
  .SaveToFile batPath, adSaveCreateOverWrite
  .Close
End With

'Se ejecuta el archivo batch
Set WhShell = CreateObject("WScript.Shell")
WhShell.Run chr(34) & batPath & Chr(34), 0
Set WhShell = Nothing