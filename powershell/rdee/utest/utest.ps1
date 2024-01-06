#Requires -Version 7

# This script aims to test the functions in <module:rdee>
# by roadelse

# 2024-01-02    add unittests for <Assert>, <deepcopy> and <Update-Hashtable>


Describe "rdeeToolkit powershell libirary unit tests" {

    BeforeAll {
        Import-Module "$PSScriptRoot\..\..\rdee"
    }

    Context "Basic" {
        It "Assert" {
            Assert (2 -gt 1) | Should -Be $null
        }

        It "deepcopy" {
            $ht1 = @{a = 1; b = @{c = 2; d = 3 } }
            $ht2 = deepcopy $ht1
            $ht1.b.c = 4
            $ht2.a | Should -Be 1
            $ht2.b.c | should -Be 2
            $ht2.b.d | should -Be 3
        }

        It "Update-Hashtable" {
            $ht1 = @{a = 1; arr1 = @(1, 2, 3) }
            $ht2 = @{a = 3; b = @{c = 2; d = 3 }; arr1 = @(4, 4, 5) }
            Update-HashTable $ht1 $ht2
            $ht1.a | Should -Be 3
            $ht1.b.c | Should -Be 2
            $ht1.arr1.Count | Should -Be 6
            $ht2.b.c = 999
            $ht1.b.c | Should -Be 999
            # -----------------------------------
            $ht1 = @{a = 1; arr1 = @(1, 2, 3) }
            Update-HashTable $ht1 $ht2 -replace
            $ht1.arr1.Count | Should -Be 3
            # -----------------------------------
            $ht1 = @{a = 1; arr1 = @(1, 2, 3) }
            Update-HashTable $ht1 $ht2 -arrayUniq
            $ht1.arr1.Count | Should -Be 5
            # -----------------------------------
            $ht1 = @{a = 1; arr1 = @(1, 2, 3) }
            $ht2 = @{a = 3; b = @{c = 2; d = 3 }; arr1 = @(4, 4, 5) }
            Update-HashTable $ht1 $ht2 -deep
            $ht2.b.c = 999
            $ht1.b.c | Should -Be 2
        }
    }

    AfterAll {
        Remove-Module rdee
    }
}

