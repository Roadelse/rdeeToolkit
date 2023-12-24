
Function createShortcut($src, $dst, [string]$icon = "none"){
    # echo "src=$src, ddst=$ddst"
    $WScriptShell = New-Object -ComObject WScript.Shell
    
    # $dst = $dst + ".lnk"
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


$p1 = $args[0]
$p2 = $args[1]
# $item = Get-Item $p1
# $dst =(Get-Location).Path + "\" + $item.BaseName + ".lnk"
# echo $dst.GetType().FullName

createShortcut $p1 $p2