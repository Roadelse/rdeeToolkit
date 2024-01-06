#Requires AutoHotkey v2.0

#include <JXON>

; >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> basic function
ArrayEqual(a1, a2){
    ; works only for 1-d array with scalar elements

    ; Check if both arrays have the same length
    if a1.Length != a2.Length
        return false

    ; Check if corresponding elements in both arrays are equal
    for index, item in a1 {
        if (item != a2[index])
            return false
    }

    ; If the function hasn't returned false yet, the arrays are equal
    return true
}


; >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> path-relative functions
GetBaseName(path) {
    ;;; file name cannot contain "/" or "\"
    parts := StrSplit(path, ["\", "/"])
    return parts[parts.Length]
}



; >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> windows-relative function
GetActiveWindowInfo() {
    ;;; window info: [exe_name, url]


    procpath := WinGetProcessPath("A")
    ; ----------------------- for file explorers
    ; Check if the active window is a File Explorer window
    if (WinActive("ahk_class CabinetWClass")) {
        ; Try to get the path of the active Explorer window
        for window in ComObject("Shell.Application").Windows() {
            try {
                if (window.HWND = WinActive("A")) {
                    path := window.Document.Folder.Self.Path
                    return [procpath, path]
                }
            }
        }
    }

    ; ----------------------- for internet explorer
    ; If the active window is not an Explorer window, check if it's a Chrome window
    if (WinActive("ahk_exe chrome.exe") or WinActive("ahk_exe 360ChromeX.exe") or WinActive("ahk_exe msedge.exe")) {
        ; Store the current contents of the clipboard
        ; old_clipboard := ClipboardAll

        ; Empty the clipboard
        A_Clipboard := ""

        ; Send Ctrl+L to select the address bar, then Ctrl+C to copy the URL
        Send("^l")
        Sleep(100)
        Send("^c")

        ; Wait for the clipboard to contain text
        ClipWait(2)

        ; Store the URL
        url := A_Clipboard

        ; Restore the old clipboard
        ; Clipboard := old_clipboard

        return [procpath, url]
    }


    ; ----------------------- for text editor
    if (WinActive("ahk_exe sublime_text.exe")) {
        ti := WinGetTitle("A")
        if (InStr(ti, " • - Sublime")) {  ; >- return sublime exe for temporary file
            return [procpath, WinGetProcessPath("A")]
        } else {  ; >- return file path for saved, solid file
            filepath := SubStr(ti, 1, -15)
            return [procpath, filepath]
        }
    }


    ; ----------------------- for office
    if (WinActive("ahk_exe WINWORD.EXE")){
        word := ComObjActive("Word.Application")
        return [procpath, word.ActiveDocument.FullName]
    }

    if (WinActive("ahk_exe EXCEL.EXE")){
        excel := ComObjActive("Excel.Application")
        return [procpath, excel.ActiveWorkbook.FullName]
    }

    if (WinActive("ahk_exe POWERPNT.EXE")){
        ppt := ComObjActive("PowerPoint.Application")
        return [procpath, ppt.ActivePresentation.FullName]
    }


    ; >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> return the process executable path, for neither explorer nor web-browser. By now, it cannot resolve the opened file path in some apps, such as excel, sublime, .... To be developed

    return [procpath, ""]
}


startswith(string, prefix) {
    return SubStr(string, 1, StrLen(prefix)) == prefix
}

mkdir_and_run(path){
    DirCreate(path)
    Run(path)
}
