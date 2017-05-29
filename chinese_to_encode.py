# coding=utf8

import sys

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python {cmd} <chinese string>".format(cmd=sys.argv[0]))
        exit(-1)

    value = sys.argv[1]
    print({'encode': value.decode('utf8')})
