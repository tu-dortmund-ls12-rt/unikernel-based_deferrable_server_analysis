#!/usr/bin/env python3

import sys
import os
import getopt
from res import benchmark, our_analysis, rtc_cb
import pickle
from multiprocessing import Pool


# from res import benchmark


def print_usage():
    print('test.py -s <switch>')


def check_or_make_directory(dirname):
    if not os.path.exists(dirname):
        os.makedirs(dirname)
        print(f'Directory {dirname} created')


def write_data(filename, data):
    file = open(filename, 'wb')
    pickle.dump(data, file)
    file.close()
    print(f'Data written to {filename}')


def load_data(filename):
    file = open(filename, 'rb')
    data = pickle.load(file)
    file.close()
    print(f'Data loaded from {filename}')
    return data


if __name__ == "__main__":

    num_processors = 1

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

    if code_switch == '1':
        num_systems = 100

        # Create systems:
        check_or_make_directory('data/1setup')
        systems = benchmark.make_system(10, 0.1, 0.4, listof=num_systems)
        write_data(f'data/1setup/systems{code_switch}.pkl', systems)

        # Makes experiments
        with Pool(num_processors) as p:
            res_our = p.map(our_analysis.wcrt_analysis, systems)

        with Pool(num_processors) as p:
            res_rtc = p.map(rtc_cb.wcrt_analysis, systems)

        check_or_make_directory('data/2results')
        write_data(f'data/2results/res_our{code_switch}.pkl', res_our)
        write_data(f'data/2results/res_rtc{code_switch}.pkl', res_rtc)

        # Plot data
