# coding=utf-8


def split_by_true_sep(s, sep, skips = {'(' : ')', '[' : ']', '{' : '}', '"' : '"', "'" : ":"}):
    i = 0
    j = 0
    in_skip = False
    l_mark = None
    rst = []
    while i < len(s):
        if in_skip:
            if s[i:].startswith(skips[l_mark]):
                in_skip = False
                i += len(skips[l_mark])
                continue
        else:
            for lm in skips:
                if s[i:].startswith(lm):
                    in_skip = True
                    l_mark = lm
                    i += len(lm)
                    continue

            if s[i:].startswith(sep):
                rst.append(s[j:i])
                i += len(sep)
                j = i
                continue
        i += 1

    if j < len(s):
        rst.append(s[j:i])

    return rst