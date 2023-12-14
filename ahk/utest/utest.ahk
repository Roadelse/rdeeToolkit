
; This script is used to do unit-test for libraries in ahk.rdee, including custom lib and 3rd-party lib

#include <rdee>
#include <JXON>

; a := Map("hello", 1, "wa", 2)
; msgbox(a['wa'])


F4::
{

    reSave()
}

F5::
{
    reGoto()
}

F6::
{
    rob()
}

F1::
{
    MsgBox("Hello AHK")
}

F3::
{
    MsgBox(GetActiveWindowInfo())
}

F2::
{
    InputBoxObj := InputBox("Test Case:", "Choose your test")
    if StrUpper(InputBoxObj.Value) = "JXON" or StrUpper(InputBoxObj.Value) = "JSON"{
        test_JXON()
        MsgBox("JSON test pass!")
    }
    else
        MsgBox("Unknown test case: " . StrUpper(InputBoxObj.Result))
}

test_JXON(){
    clrs := Map()
    clrs["Red"] := "1"
    clrs["Green"] := "a"
    clrs["Blue"] := "~"
    var := jxon_dump(clrs, indent:=0)
    if var != '{"Blue":"~","Green":"a","Red":"1"}'{
        MsgBox("Error! Unexpected JXON-dumped string")
        Exit 1
    }

    str2 := "[1,2,3,4]"
    obj := jxon_load(&str2)
    if ! ArrayEqual(obj, [1,2,3,4]){
        MsgBox("Error! Unexpected JXON-loaded string")
        Exit 1
    }
}