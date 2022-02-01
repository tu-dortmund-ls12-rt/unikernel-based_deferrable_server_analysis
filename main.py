#!/usr/bin/env python3

import sys
import os
import getopt
from res import benchmark, our_analysis, rtc_cb, plot
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
    switch_1 = True
    switch_2 = True
    switch_3 = True

    num_systems = 100
    num_servers = 10

    # =====args=====
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hn:s:o:")
    except getopt.GetoptError:
        print_usage()
        sys.exit(2)
    if len(opts) == 0:
        print_usage()
        sys.exit()
    for opt, arg in opts:
        if opt == '-h':
            print_usage()
            sys.exit()
        elif opt in ('-s',):  # define which part of the code is being executed
            code_switch = arg
        elif opt == '-o':
            # only certain steps being executed
            if '1' not in arg:
                switch_1 = False
            if '2' not in arg:
                switch_2 = False
            if '3' not in arg:
                switch_3 = False
        elif opt == '-n':  # number of servers per system
            num_servers = int(arg)

    if code_switch == '1':

        if switch_1:
            # Create systems:
            check_or_make_directory('data/1setup')
            systems = benchmark.make_system(num_servers, 0.1, 0.4, listof=num_systems)
            write_data(f'data/1setup/systems{code_switch}_{num_servers=}.pkl', systems)

        if switch_2:
            if not switch_1:
                # Load data
                systems = load_data(f'data/1setup/systems{code_switch}_{num_servers=}.pkl')
            # Makes experiments
            with Pool(num_processors) as p:
                res_our = p.map(our_analysis.wcrt_analysis, systems)

            with Pool(num_processors) as p:
                res_rtc = p.map(rtc_cb.wcrt_analysis, systems)

            check_or_make_directory('data/2results')
            write_data(f'data/2results/res_our{code_switch}_{num_servers=}.pkl', res_our)
            write_data(f'data/2results/res_rtc{code_switch}_{num_servers=}.pkl', res_rtc)

        if switch_3:
            if not switch_2:
                # Load data
                res_our = load_data(f'data/2results/res_our{code_switch}_{num_servers=}.pkl')
                res_rtc = load_data(f'data/2results/res_rtc{code_switch}_{num_servers=}.pkl')
            # Plot data
            flat_res_our = [entry for lst in res_our for entry in lst]
            flat_res_rtc = [entry for lst in res_rtc for entry in lst]
            # breakpoint()
            assert len(flat_res_our) == len(flat_res_rtc)
            data = [e1 / e2 for e1, e2 in zip(flat_res_our, flat_res_rtc)]

            check_or_make_directory('data/3plots')
            plot.plot(data, f'data/3plots/plot{code_switch}_{num_servers=}.pdf',
                      title=f'plot{code_switch}_{num_servers=}',
                      xticks=['WCRT our / WCRT their'])

    if code_switch == '2':
        # plot several boxplots
        num_servers = 10
        res_our_1 = load_data(f'data/2results/res_our{1}_{num_servers=}.pkl')
        res_rtc_1 = load_data(f'data/2results/res_rtc{1}_{num_servers=}.pkl')
        flat_res_our_1 = [entry for lst in res_our_1 for entry in lst]
        flat_res_rtc_1 = [entry for lst in res_rtc_1 for entry in lst]
        assert len(flat_res_our_1) == len(flat_res_rtc_1)
        data_1 = [e1 / e2 for e1, e2 in zip(flat_res_our_1, flat_res_rtc_1)]

        num_servers = 50
        res_our_2 = load_data(f'data/2results/res_our{1}_{num_servers=}.pkl')
        res_rtc_2 = load_data(f'data/2results/res_rtc{1}_{num_servers=}.pkl')
        flat_res_our_2 = [entry for lst in res_our_2 for entry in lst]
        flat_res_rtc_2 = [entry for lst in res_rtc_2 for entry in lst]
        assert len(flat_res_our_2) == len(flat_res_rtc_2)
        data_2 = [e1 / e2 for e1, e2 in zip(flat_res_our_2, flat_res_rtc_2)]

        num_servers = 100
        res_our_3 = load_data(f'data/2results/res_our{1}_{num_servers=}.pkl')
        res_rtc_3 = load_data(f'data/2results/res_rtc{1}_{num_servers=}.pkl')
        flat_res_our_3 = [entry for lst in res_our_3 for entry in lst]
        flat_res_rtc_3 = [entry for lst in res_rtc_3 for entry in lst]
        assert len(flat_res_our_3) == len(flat_res_rtc_3)
        data_3 = [e1 / e2 for e1, e2 in zip(flat_res_our_3, flat_res_rtc_3)]

        check_or_make_directory('data/3plots')
        plot.plot([data_1, data_2, data_3], f'data/3plots/plot{code_switch}_combined.pdf',
                  title=f'plot{code_switch}',
                  xticks=['10', '50', '100'])
