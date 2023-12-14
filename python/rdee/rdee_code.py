# coding=utf-8

#**********************************************************************
# this function is used to perform pretty and prescribed skeleton comments
#**********************************************************************
def norm_skComments(C, level = 1, language = 'ncl') : # normalize skeleton comments
    import sys

    if language == 'ncl' :
        cl = ';' # comment label
    elif language == 'python':
        cl = '#'
    else:
        print('unknwon language : {}'.format(language))
        sys.exit(1)

    if level == 1: # final 60
        charL = '>'
        charR = '<'
        lenCharL = ((59 - 4) - len(C)) // 2
        lenCharR = 59 - 4 - len(C) - lenCharL
        res = "{} {} {} {}".format(cl, charL * lenCharL, C, charR * lenCharR)
    elif level == 2:
        res = "{} {} {}".format(cl, '=' * 15, C)
    elif level == 3:
        res = "{} {} {}".format(cl, '~' * 10, C)
    elif level == 4:
        res = "{} {} {}".format(cl, '-' * 5, C)

    print(res)



#**********************************************************************
# this function is used to check if a function has a return value
#**********************************************************************
def has_return_value(func):
    import inspect
    import ast
    tree = ast.parse(inspect.getsource(func))
    return any(isinstance(node, ast.Return) for node in ast.walk(tree))
