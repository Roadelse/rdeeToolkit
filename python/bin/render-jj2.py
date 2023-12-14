#!/usr/bin/env python3
# coding=utf-8

import os, sys, os.path
import jinja2 as jj2


if __name__ == '__main__':
    assert len(sys.argv) > 1  # all arguments are target files

    if 'jj2_lsp' in os.environ:
        lsp = os.environ['jj2_lsp']
    else:
        lsp = None

    if os.path.exists('jj2_context.py'):
        sys.path.append('.')
        import jj2_context
        ctt = jj2_context.ctt
    else:
        ctt = None

    for infile in sys.argv[1:]:

        assert os.path.exists(infile), f'{infile} doesn''t exist'
        file_abspath = os.path.abspath(infile)

        inDir = os.path.dirname(file_abspath)

        fbname = os.path.basename(file_abspath)
        oName, ext = os.path.splitext(file_abspath)

        assert ext == '.jj2'

        content = open(infile).read()

        template = jj2.Template(content, line_statement_prefix=lsp)

        if ctt:
            content2 = template.render(ctt)
        else:
            content2 = template.render()
        # print(content2)
        with open(oName, 'w') as f:
            f.write(content2)