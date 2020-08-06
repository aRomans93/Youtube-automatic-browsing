Dim taskName, xmlFileName, vbsFileName, folderPath, pythonFileName, chromeDriver, userProfilePath, strPath, sCurPath
Const Overwrite = True
Set objShell = CreateObject("WScript.Shell")
Set objFSO = CreateObject("Scripting.FileSystemObject")

'El nombre que le asignaremos a la tarea
taskName = "youtube_test"

'El nombre del XML para configurar la tarea
xmlFileName = "schedule_test.xml"

'El nombre del archivo vbs en el cual se actualizaran los argumentos
vbsFileName = "argumentos_test.vbs"

'La ruta a la cual se moveran nuestros archivos
'Lo que continua despues de C:\Users\user.profile
folderPath = "\seguritech_youtube"

'El nombre de nuestro script de python
pythonFileName = "youtube_test.py"

'El nombre de nuestro archivo chromedriver
chromeDriver = "chromedriver.exe"

'Instalacion de numpy con pip
objShell.Run "pip install numpy", 0, false
WScript.Sleep(100000)

'Instalacion de selenium con pip
objShell.Run "pip install selenium", 0, false
WScript.Sleep(100000)

'Instalacion de scrapy con pip
objShell.Run "pip install scrapy", 0, false
WScript.Sleep(100000)

'Creamos la carpeta

'Obtenemos la ruta hacia el perfil del usuario
userProfilePath = objShell.ExpandEnvironmentStrings("%UserProfile%")

folderPath = userProfilePath & folderPath
If Not objFSO.FolderExists(folderPath) Then
  objFSO.CreateFolder folderPath
End If

'Copiamos nuestros archivos a la nueva carpeta

'Primero obtenemos la ruta donde actualmente estan nuestros archivos
strPath = Wscript.ScriptFullName
Set objFile = objFSO.GetFile(strPath)
sCurPath = objFSO.GetParentFolderName(objFile) 
sCurPath = sCurPath & "\"

folderPath = folderPath & "\"
objFSO.CopyFile sCurPath&vbsFileName, folderPath, Overwrite
objFSO.CopyFile sCurPath&pythonFileName, folderPath, Overwrite
objFSO.CopyFile sCurPath&chromeDriver, folderPath, Overwrite

'Creamos la tarea programada
Dim xmlPath, vbsPath, strArgs_createTask

'Primero modificamos el XML con la configuracion utilizada para crear la tarea
xmlPath = sCurPath & xmlFileName

Set xmlDoc = CreateObject("Microsoft.XMLDOM")
xmlDoc.Async = "False"
xmlDoc.load xmlPath

'Locate the desired node
'Note the use of XPATH instead of looping over all the child nodes
Set nNode = xmlDoc.selectsinglenode ("//Task/Actions/Exec/Command")

'Set the node text with the new value
vbsPath = folderPath & vbsFileName
nNode.text = vbsPath

'Save the xml document with the new settings.
strResult = xmldoc.save(xmlPath)

'Comando para crear la tarea
strArgs_createTask = "schtasks /create /tn " & taskName & " /XML " & xmlPath
objShell.Run strArgs_createTask, 0, false
set objShell = Nothing