---
title: Ref code
date: '2025-12-10'
tags:
- shell
- 文件
- Go
- 类型
- 递归
- HTTP
- HTTPS
- IP
- HTML
- tac
- nc
- Windows
- Git
---

https://gigazine.net/news/20250524-windows-moricons-dll/?utm_source=chatgpt.com
https://gigazine.net/news/20250524-windows-moricons-dll/?utm_source=chatgpt.com

https://windowsforum.com/threads/the-enduring-legacy-of-windows-moricons-dll-nostalgia-compatibility-and-digital-heritage.365339/?utm_source=chatgpt.com

https://retrocomputing.stackexchange.com/questions/6705/what-are-the-software-logos-in-moricons-dll

https://xpdll.nirsoft.net/moricons_dll.html?utm_source=chatgpt.com



```vb
Option Explicit

Dim fso, outFile
Set fso = CreateObject("Scripting.FileSystemObject")
Set outFile = fso.CreateTextFile("C:\icon_files.txt", True)

' 扫描 Windows 系统目录
ListIcons "C:\Windows"

outFile.Close
MsgBox "完成！带图标的文件列表已保存到 C:\icon_files.txt"

' --------------------------
' 递归遍历目录
' --------------------------
Sub ListIcons(path)
    Dim folder, file, subfolder
    On Error Resume Next
    Set folder = fso.GetFolder(path)

    ' 遍历文件
    For Each file In folder.Files
        If IsIconFile(file.Path) Then
            If HasIcon(file.Path) Then
                outFile.WriteLine file.Path
            End If
        End If
    Next

    ' 遍历子文件夹
    For Each subfolder In folder.SubFolders
        ListIcons subfolder.Path
    Next
End Sub

' --------------------------
' 判断文件是否属于可带图标类型
' --------------------------
Function IsIconFile(filepath)
    Dim ext
    ext = LCase(fso.GetExtensionName(filepath))
    Select Case ext
        Case "exe", "dll", "ocx", "cpl", "scr", "ico"
            IsIconFile = True
        Case Else
            IsIconFile = False
    End Select
End Function

' --------------------------
' 检查文件是否带图标
' 通过尝试调用 shell32.dll ExtractIconA
' --------------------------
Function HasIcon(filepath)
    Dim shell, icon
    Set shell = CreateObject("WScript.Shell")

    On Error Resume Next
    ' 调用 ExtractIconA 尝试获取图标
    icon = shell.Run("rundll32.exe shell32.dll,ExtractIconA 0, """ & filepath & """, 0", 0, True)

    If Err.Number = 0 Then
        HasIcon = True
    Else
        HasIcon = False
        Err.Clear
    End If
End Function

```