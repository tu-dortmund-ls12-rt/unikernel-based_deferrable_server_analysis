#!/usr/bin/env python3
"""Synthetic creation of servers and tasks."""

import numpy as np
import random
import math


class System:
    """One system that has to be analysed."""

    def __init__(self, servers, tasks):
        # check if length matches
        assert len(servers) == len(tasks)
        self.servers = servers
        self.tasks = tasks

    def server_task_tuples(self):
        return zip(self.servers, self.tasks)

    def __str__(self):
        complete_str = ''
        for s, t in zip(self.servers, self.tasks):
            complete_str += str(s) + ' | ' + str(t) + '\n'
        complete_str += f'Server utilization: {sum(s.budget / s.period for s in self.servers)}\n'
        complete_str += f'Task utilzation: {sum(t.wcet / t.min_iat for t in self.tasks)}'
        return complete_str

    @staticmethod
    def help():
        print('System(<list of servers>, <list of tasks>')
        print('Priority of the servers is in descending order.')
        print('Only one task per server.')
        print('var: servers, tasks')
        print('fun: server_task_tuples')


class Server:
    """A deferrable server (DS)."""

    def __init__(self, period, budget):
        self.period = period
        self.budget = budget

    def __str__(self):
        return 'Server period: ' + str(self.period) + ' Server budget: ' + str(self.budget)

    @staticmethod
    def help():
        print('Server(<replenishment period>, <budget of the server>')
        print('var: period, budget')


class Task:
    """A tasks."""

    def __init__(self, minimum_inter_arrival_time, wcet):
        self.min_iat = minimum_inter_arrival_time
        self.wcet = wcet

    def __str__(self):
        return 'Task min_iat: ' + str(self.min_iat) + ' Task wcet: ' + str(self.wcet)

    @staticmethod
    def help():
        print('Task(<minimum inter arrival time>, <worst case execution time>')
        print('var: min_iat, wcet')


'''reference: from https://github.com/tu-dortmund-ls12-rt/SSSEvaluation'''


def uunifast(n, U_avg):
    """UUnifast creation of utilization vector.
    From: https://github.com/tu-dortmund-ls12-rt/SSSEvaluation"""
    USet = []
    sumU = U_avg
    for i in range(n - 1):
        nextSumU = sumU * math.pow(random.random(), 1 / (n - i))
        USet.append(sumU - nextSumU)
        sumU = nextSumU
    USet.append(sumU)
    return USet


# def lognuniform(low=0, high=1, size=None, base=np.e):
#     return np.power(base, np.random.uniform(low, high, size))

def loguniform(n, Tmin=1, Tmax=100, base=10):
    TSet = []
    for i in range(n):
        TSet.append(math.pow(base, random.uniform(math.log(Tmin, base), math.log(Tmax, base))))
    return TSet


def make_system(n_min, n_max, U_min, U_max, task_mit=[1.0, 1.5], task_wcet=[0.5, 1], listof=None):
    if listof is not None:
        return [make_system(n_min, n_max, U_min, U_max, task_mit=task_mit, task_wcet=task_wcet) for _ in range(listof)]

    # Servers
    n = random.randint(n_min, n_max)  # number of servers for this system
    P = loguniform(n)  # replenishment periods
    U = uunifast(n, random.uniform(U_min, U_max))  # utilizations
    servers = [Server(p, p * u) for p, u in zip(P, U)]
    servers.sort(key=lambda x: x.period)  # order servers by replenishment period

    # Tasks
    tasks = [Task(s.period * random.uniform(task_mit[0], task_mit[1]),
                  s.budget * random.uniform(task_wcet[0], task_wcet[1])) for s in servers]

    # System
    return System(servers, tasks)


if __name__ == '__main__':
    """Some testing."""

    tests = range(20)

    if 1 in tests:
        # Test 1: Correct behaviour of loguniform distribution.
        TSet = loguniform(1000)
        print('1 <= t < 10:', sum(1 for t in TSet if 1 <= t < 10))
        print('10 <= t <= 100:', sum(1 for t in TSet if 10 <= t <= 100))
        print('t < 1 or t > 100:', [t for t in TSet if t < 1 or t > 100])
    if 2 in tests:
        sy = make_system(3, 3, 0.1, 0.2)
        breakpoint()
    if 3 in tests:
        systems = make_system(3, 3, 0.1, 0.2, listof=2)
        breakpoint()
