# coding=utf-8


# ................. standard lib
import sys
import argparse
# ................. project lib
from . import utest



def main():
    parser = argparse.ArgumentParser(description="""library test & information""")
    parser.add_argument('--test', '-t', nargs='?', const='all', default=False, help='select test target, support TestCase and specific test, such as TC,TC.test, use "," to combine several tests')
    args = parser.parse_args()
    # print(args.test)
    if args.test:
        utest.run(args.test)


if __name__ == '__main__':
    main()
