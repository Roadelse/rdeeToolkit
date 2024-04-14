# coding=utf-8


# ................. standard lib
import sys
import argparse
# ................. project lib
import rdee


def main():
    parser = argparse.ArgumentParser(description="""library test & information""")
    parser.add_argument('--utest', '-u', nargs='*', default=False, help='select test target')
    parser.add_argument('--remainTest', action="store_true", help='utest will not delete the test directory if this option is set')
    parser.add_argument('--func', '-f', nargs='*', default=False, help='select test target')

    args = parser.parse_args()
    # print(args.utest)
    if args.utest is not False:
        from . import utest
        utest.run(args.utest, args.remainTest)
        return
    
    if args.func is not False:
        func = getattr(rdee, args.func[0])
        # print(func)
        print(func(*args.func[1:]))



if __name__ == '__main__':
    main()
