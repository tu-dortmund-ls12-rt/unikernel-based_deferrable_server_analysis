#!/usr/bin/env python3

import sys
import os
import getopt


def print_usage():
    print('test.py -s <switch>')


def check_or_make_directory(dirname):
    if not os.path.exists(dirname):
        os.makedirs(dirname)


if __name__ == "__main__":

    # =====args=====
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hs:")
    except getopt.GetoptError:
        print_usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print_usage()
            sys.exit()
        elif opt in ("-s",):  # define which part of the code is being executed
            code_switch = arg
