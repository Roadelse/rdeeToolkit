#Requires -Version 7

# >>>>>>>>>>>>>>>>>>>>>>>>>>> [prepare]
param(

)

$myDir = $PSScriptRoot


# >>>>>>>>>>>>>>>>>>>>>>>>>>> [python]
$pylib = [System.IO.Path]::GetFullPath("$myDir\..\rdeeEnv")
[Environment]::SetEnvironmentVariable('PYTHONPATH', "$pylib", [EnvironmentVariableTarget]::User)
[Environment]::SetEnvironmentVariable('pipsrc1', "https://pypi.tuna.tsinghua.edu.cn/simple", [EnvironmentVariableTarget]::User)
# <<<

# >>>>>>>>>>>>>>>>>>>>>>>>>>> [powershell]
$pwshlib = [System.IO.Path]::GetFullPath("$myDir\..\powershell")
$psmp_current = [System.Environment]::GetEnvironmentVariable("PSModulePath")
# $psmp_current_user = [System.Environment]::GetEnvironmentVariable("PSModulePath", [System.EnvironmentVariableTarget]::User)
# Write-Output $pwshlib
# exit
if (-not $psmp_current.Contains($pwshlib)) {
    [Environment]::SetEnvironmentVariable('PSModulePath', "$pwshlib", [EnvironmentVariableTarget]::User)
}
# <<<

# >>>>>>>>>>>>>>>>>>>>>>>>>>> [ahk]
$ahk_install_script = [IO.Path]::GetFullPath("$myDir\..\ahk\install.ps1")
Start-Process powershell.exe "-File $ahk_install_script" -Verb RunAs -WindowStyle Hidden
# <<<

# >>>>>>>>>>>>>>>>>>>>>>>>>>> [bin]
$rdeeDir = "D:\XAPP\rdee"
$rdeeBin = "$rdeeDir\bin"
New-Item -ItemType Directory -Path $rdeeBin -Force

Get-ChildItem $myDir\..\bin -Include "*.py", "*.ps1" -Recurse -File | ForEach-Object {
    $fp = [IO.Path]::GetFullPath($_)
    $name = $_.Name
    New-Item -ItemType SymbolicLink -Target "$fp" -Path "$rdeeBin\$name" -Force
}
$env_path_user = [System.Environment]::GetEnvironmentVariable("Path", [System.EnvironmentVariableTarget]::User)
[Environment]::SetEnvironmentVariable('Path', ("$env_path_user" + ";$rdeeBin"), [EnvironmentVariableTarget]::User)

# <<<


# >>>>>>>>>>>>>>>>>>>>>>>>>>> [profile]
$settings = @"
# >>>>>>>>>>>>>>>>>>>>>>>>>>> [rdeeToolkit]
Import-Module rdee
# <<<

"@

Write-Output "Please add the code below into $profile"
Write-Output $settings