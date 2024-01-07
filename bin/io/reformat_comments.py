#!/usr/bin/env python
# coding=utf-8

import argparse
import os, os.path
import rdee


def main():
    parser = argparse.ArgumentParser(description="""reformat comments""")
    parser.add_argument('target_file', type=str, help='target file')
    args = parser.parse_args()

    target_file = args.target_file
    assert os.path.exists(target_file), f'Error! Cannot find target file: {target_file}'

    target_content = open(target_file).read()
    result_content = rdee.reformat_comments(target_content)
    with open(target_file, 'w') as f:
        f.write(result_content)

if __name__ == '__main__':
    main()