
# This script is used to install all libraries, including my custom and 3rd-party-libs, into the target place, that is, dir(~AHK.exe)/Lib

#code to make sure the script is running as admin
If (-NOT ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    # Relaunch as an elevated process:
    Start-Process powershell.exe "-ExecutionPolicy", "bypass", "-File", ('"{0}"' -f $MyInvocation.MyCommand.Path) -Verb RunAs
    exit
}
Set-Location -Path $PSScriptRoot

$ahk_prog_dir = "C:\Program Files\AutoHotkey"
$curDir = $(Get-Location).Path
Write-Output "curDir is $curDir"

# >>>>>>>>>> 1. check the AHK installation
if (!(Test-Path $ahk_prog_dir)) {
    Write-Output "Error! Cannot find AutoHotKey program in $ahk_prog_dir"
    exit
}

$ahk_exe_dir = "C:\Program Files\AutoHotkey\v2"
if (!(Test-Path $ahk_exe_dir)) {
    Write-Output "Error! Cannot find AutoHotKey executable directory in $ahk_exe_dir"
    exit
}

if (!(Test-Path "$ahk_exe_dir\Lib")) {
    New-Item -ItemType Directory $ahk_exe_dir\Lib
}
Remove-Item "$ahk_exe_dir\Lib\*"


# >>>>>>>>>> 2. handle custom lib
if (!(Test-Path "$ahk_exe_dir\Lib\rdee.ahk")) {
    New-Item -ItemType SymbolicLink -Path $ahk_exe_dir\Lib\rdee.ahk -Target $curDir/myLibs/rdee.ahk
}

# >>>>>>>>>> 3. handle 3rd-party libs
$libs3p = Get-ChildItem -Path $curDir\3rd-party-libs\*ahk -File
foreach ($file in $libs3p) {
    if (!(Test-Path $ahk_exe_dir\Lib\$($file.Name))) {
        New-Item -ItemType SymbolicLink -Path $ahk_exe_dir\Lib\$($file.Name) -Target $curDir\3rd-party-libs\$($file.Name)
    }
}

Read-Host -Prompt "Press Enter to exit"
