#Requires -Version 7


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