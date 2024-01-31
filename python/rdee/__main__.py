# coding=utf-8


# ................. standard lib
import sys
import argparse
# ................. project lib
from . import utest



def main():
    parser = argparse.ArgumentParser(description="""library test & information""")
    parser.add_argument('--utest', '-u', nargs='*', default=False, help='select test target')
    args = parser.parse_args()
    # print(args.utest)
    if args.utest is not False:
        utest.run(args.utest)


if __name__ == '__main__':
    main()
