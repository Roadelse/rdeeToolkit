#Requires -Version 7


Set-Alias -Name 'vi' -Value 'vim'

function _cdUp {
    [Alias('..')]
    param()
    Set-Location ..
}

function _cdUpUp {
    [Alias('...')]
    param()
    Set-Location ..\..
}

function which {
    param(
        [string]$name
    )
    Get-Command $name
}

function touch {
    param(
        [string]$name
    )
    New-Item -ItemType File -Path $name
}

function cdG {
    Set-Location D:\recRoot\GitRepos
}

function cdO {
    Set-Location C:\Users\$env:UserName\OneDrive\recRoot
}

function cdB {
    Set-Location D:\BaiduSyncdisk\recRoot
}

function cdR {
    Set-Location D:\recRoot
}

function cdU {
    Set-Location C:\Users\$env:UserName
}

function cdD {
    Set-Location C:\Users\$env:UserName\Desktop
}


function admin {
    if ($PSVersionTable.PSEdition -eq "Core") {
        Start-Process pwsh.exe -WorkingDirectory $pwd -Verb RunAs
    } else {
        Start-Process powershell.exe -ArgumentList "-NoExit", "-Command Set-Location $pwd" -Verb RunAs
    }
}

function run {
    param(
        [string]$file
    )
    $target = Get-Command $file 2>$null
    if ($null -eq $target) {
        $target = Get-Item $file 2>$null
        if ($null -eq $target) {
            Write-Error "Cannot find $file"
            return
        } else {
            $target_file = $target.FullName
        }
    } else {
        $target_file = $target.Source
    }

    if ($target_file.EndsWith('.py')) {
        python $target_file
    } elseif ($target_file.EndsWith('.py')) {
        $target_file
    } else {
        Write-Error "Unknown file type: $target_file"
        return
    }
}


function Update-Hashtable {
    <#
    .SYNOPSIS
    update a hashtable from another hashtable
    #>
    param(
        [Parameter(Mandatory = $true)]
        [hashtable]$base,
        [Parameter(Mandatory = $true)]
        [hashtable]$target,
        [switch]$replace,
        [switch]$arrayUniq,
        [switch]$deep
    )
    foreach ($key in $target.Keys) {
        # Write-Output $key
        # >>>>>>>>> for the condition that $base.$key doesn't exist or -replace switched
        if ($replace -or $null -eq $base.$key) {
            if ($deep) {
                $base.$key = deepcopy $target.$key
            } else {
                $base.$key = $target.$key
            }
            continue
        }

        # >>>>>>>>> for the condition that $base.$key exists
        if ($base.$key -is [hashtable]) {
            Assert ($target.$key -is [hashtable])
            Update-Hashtable $base.$key $target.$key -replace:$replace -arrayUniq:$arrayUniq -deep:$deep
        } elseif ($base.$key -is [array]) {
            $base.$key += $target.$key
            if ($arrayUniq) {
                [array]$base.$key = [System.Collections.Generic.HashSet[object]]$base.$key
            }
        } else {
            $base.$key = $target.$key
        }
    }
}

function Assert {
    <#
    .SYNOPSIS
    assert 
    #>
    param(
        [Parameter(Mandatory = $true)]
        [bool]$cond,
        [string]$errmsg
    )

    if (-not $cond) {
        Write-Error $errmsg -ErrorAction Stop
    }
}

function deepcopy ($InputObject) {
    <#
    .SYNOPSIS
    Use the serializer to create an independent copy of an object, useful when using an object as a template
    #>
    return [System.Management.Automation.PSSerializer]::Deserialize(
        [System.Management.Automation.PSSerializer]::Serialize(
            $InputObject
        )
    )
}