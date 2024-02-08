# Preface

## introduction

此处记录自用的cmake module脚本, 包含各类监测, findPackage等功能

## protocol

### messgae sign

+ custom print sign: `§`, `Alt+167`
+ temporary check or debug : `¦`, `Alt+166`
+ flow control : `>>>>>`

### colorfule message

+ Black/White : 考虑有黑底有白底的, 都不用
+ red : cmake自己的fatal error就是红色的吧, 不用red
+ yellow : 留给cmake自己的warning
+ magenta :custom输出里的 高亮 用yellow表征
+ cyna : domain specification
+ blue : *to be designed*
+ green : flow control and hint colors

### domain specification

+ module script中的message, 前面加上说明信息, 例如:`§ (rdee.python) find ...`, 括号内的以蓝色表示