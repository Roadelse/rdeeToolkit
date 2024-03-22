
param(
  [string]$from,
  [string]$to,
  [Alias("s")]
  [switch]$shortcut
)

if (-not $IsWindows){
    Write-Error "This script can only be run in Windows" -ErrorAction Stop
}

Function createShortcut($src, $dst, [string]$icon = "none"){
    # echo "src=$src, ddst=$ddst"
    $WScriptShell = New-Object -ComObject WScript.Shell
    
    if (-not $dst.Endswith(".lnk")){
      $dst = $dst + ".lnk"
    }
    # Write-Output $src
    # Write-Output $dst

    $Shortcut = $WScriptShell.CreateShortcut($dst)
    $Shortcut.TargetPath = $src
    if ($icon -ne "none"){
      $shortcut.IconLocation = $icon
    }
    #Save the Shortcut to the TargetPath
    $Shortcut.Save()
}


if ($shortcut){
  createShortcut $from $to
} else {
    New-Item -ItemType SymbolicLink -Path $to -Target $from -Force > $null
}
