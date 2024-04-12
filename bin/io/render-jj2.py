#!/usr/bin/env python3
# coding=utf-8


"""
usage: render-jj2.py [-h] [--utest] [--lsp LSP] [--context CONTEXT] [--output OUTPUT] [files ...]

render jinja2 template

positional arguments:
  files                 target files

options:
  -h, --help            show this help message and exit
  --utest, -u           do unittest
  --lsp LSP, -p LSP     set line statement prefix
  --context CONTEXT, -c CONTEXT
                        set jinja2 context file
  --output OUTPUT, -o OUTPUT
                        set output file

___________________________________________________________

2024-04-12  rebuild     | support command line argument now 
"""


import os, sys, os.path
import importlib
import argparse

import jinja2 as jj2


def load_module_from_path(module_path, module_name=None):
    """
    (borrowed from rdee-python)
    -----------------------------------
    load a module from filepath
    -----------------------------------
    2024-04-12 init
    """
    if module_name is None:
        module_name = module_path.split('/')[-1].split('.')[0]
    
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main(args):
    for infile in args.files:
        if not os.path.exists(infile):
            print(f"Warning! Cannot find {infile}, skip")
            continue

        file_abspath = os.path.abspath(infile)

        inDir = os.path.dirname(file_abspath)

        fbname = os.path.basename(file_abspath)
        oName, ext = os.path.splitext(file_abspath)
        oPath = os.path.join(args.output, oName)

        if ext != ".jj2":
            print(f"Skip {infile} whose extension is not '.jj2'")
            continue

        content = open(infile).read()

        try:
            template = jj2.Template(content, line_statement_prefix=lsp)

            if ctt:
                content2 = template.render(ctt)
            else:
                content2 = template.render()
        except:
            print(f"Error! Failed to render {infile}, skip")
            continue

        with open(oPath, 'w') as f:
            f.write(content2)


def utest():
    raise NotImplementedError

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="""render jinja2 template""")
    parser.add_argument('--utest', '-u', action="store_true", help='do unittest')
    parser.add_argument('--lsp', '-p', type=str, default=None, help='set line statement prefix') # exp | line_statement_prefix
    parser.add_argument('--context', '-c', type=str, default="jj2_context.py", help='set jinja2 context file') 
    parser.add_argument('--output', '-o', type=str, default="jj2_context.py", help='set output file') 
    parser.add_argument('files', nargs='*', default = None, help="target files")

    args = parser.parse_args()

    if args.utest:
        utest()
        sys.exit()

    if args.lsp is None:
        if 'jj2_lsp' in os.environ:
            lsp = os.environ['jj2_lsp']
        else:
            lsp = None
        if lsp is None:
            raise ValueError("Must provide lsp argument")
    else:
        lsp = args.lsp

    try:
        jj2_content = load_module_from_path(args.context)
        ctt = jj2_content.ctt
    except:
        ctt = None

    if args.files is None:
        sys.exit()

    if args.output is None:
        args.output = "."

    main(args)