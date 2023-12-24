

# echo $args.Length

echo $args[0]

$files = Get-Item $args[0]

echo $files


ForEach ($f in $files){
    echo $f.FullName
    echo $f.Name

    [void](New-Item -ItemType SymbolicLink -Value $($f.FullName) -Path $($f.Name))
}