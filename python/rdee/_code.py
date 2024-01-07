# coding=utf-8

import re

#**********************************************************************
# this function is used to perform pretty and prescribed skeleton comments
#**********************************************************************
def norm_skComment(C, level = 1, language = 'python', commentSymbol = None, style='default') : # normalize skeleton comments
    import sys

    if commentSymbol:
        cl = commentSymbol
    else:
        if language == 'ncl' :
            cl = ';' # comment label
        elif language == 'python':
            cl = '#'
        else:
            raise RuntimeError('unknwon language : {}'.format(language))

    if style == 'default':
        if level == 1: # final 60
            charL = '>'
            charR = '<'
            lenCharL = ((59 - 4) - len(C)) // 2
            lenCharR = 59 - 4 - len(C) - lenCharL
            res = "{} {} {} {}".format(cl, charL * lenCharL, C, charR * lenCharR)
        elif level == 2:
            res = "{} {} {}".format(cl, '=' * 18, C)
        elif level == 3:
            res = "{} {} {}".format(cl, '~' * 10, C)
        elif level == 4:
            res = "{} {} {}".format(cl, '.' * 3, C)

    return res
    # print(res)



#**********************************************************************
# this function aims to reformat the skeleton comments
#**********************************************************************
def reformat_comments(content, style='default'):
    if isinstance(content, str):
        lines = content.splitlines()
    elif isinstance(content, list):
        lines = content
    else:
        raise TypeError
    
    for L in lines:
        if L[0] in ('#', '!', ';', '%'):
            commentSymbol = L[0]
        elif L[:2] in ('//'):
            commentSymbol = L[:2]
        else:
            raise RuntimeError("Unknown comment type or no comment at all!")
        break

    for i in range(len(lines)):
        L = lines[i]
        if not L.lstrip().startswith(commentSymbol):
            continue
        
        rst = re.search(rf' *{commentSymbol} *<L(\d)>', L)
        if rst:
            rerst = re.search(r'( *).*?<L(\d)> (.*)', L)
            actual_comment = rerst.group(3)
            cLevel = int(rerst.group(2))
            leadingSpaces = rerst.group(1)
            lines[i] = f"{leadingSpaces}{norm_skComment(actual_comment, cLevel, commentSymbol=commentSymbol, style=style)}"
    
    return '\n'.join(lines)



#**********************************************************************
# this function is used to check if a function has a return value
#**********************************************************************
def has_return_value(func):
    import inspect
    import ast
    tree = ast.parse(inspect.getsource(func))
    return any(isinstance(node, ast.Return) for node in ast.walk(tree))



#**********************************************************************
# this function is used to check if a function has a return value
# Use dir(), pkgutil. may work as well
#**********************************************************************
def get_submodules(module, alias: str = None):
    import types
    
    assert isinstance(module, types.ModuleType)

    if not hasattr(get_submodules, 'obj_set'):
        outermost_flag = 1
        setattr(get_submodules, 'obj_set', set())

    get_submodules.obj_set.add(module.__name__)
    
    try:  #>- check fully initialized
        dir(module)
    except:
        return []
        
    # print(mod_str)
    # time.sleep(0.1)
    for img in dir(module):
        if img.startswith('_'):
            continue
        attr_str = f'module.{img}'
        try:
            attr = eval(attr_str)
        except:
            continue
        if isinstance(attr, types.ModuleType) and \
           attr.__name__ not in get_submodules.obj_set and \
           attr.__name__.startswith(module.__name__):
            # >- 1. check module; 2. ensure no circular; 3.avoid external module
            get_submodules(attr)
    
    # >>>>>>> remove the obj_set after the whole statistics
    if 'outermost_flag' in locals():
        rst = get_submodules.obj_set
        delattr(get_submodules, 'obj_set')
        if alias is not None:
            rst = {_.replace(module.__name__, alias, 1) for _ in rst}
        return list(rst)        



#**********************************************************************
# this function is used to get all submodules for target module
#**********************************************************************
def search_api(module, api: str, alias: str = None) -> list[str]:
    submodules = get_submodules(module, 'module')

    rst = []
    for sm in submodules:
        try:
            if hasattr(eval(sm), api):
                rst.append(f'{sm}.{api}')
        except:
            continue

    return [_.replace('module', module.__name__ if alias is None else alias) for _ in rst]