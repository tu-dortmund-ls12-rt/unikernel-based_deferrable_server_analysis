#!/usr/bin/env python3
"""Our analysis."""
import math


class Rplusminus:
    """Parent class for Rplus and Rminus"""

    def __init__(self, hp_servers, server):
        self.hp_servers = hp_servers
        self.server = server
        self.values = dict()
        self.evaluated_until = -1
        pass

    def _add_value(self, key, value):
        """Add one more key and value to the list."""
        assert key not in self.values or self.values[key] == value
        self.values[key] = value

    def add_values(self, lst, eval_end):
        """Add several keys and values to the list all at once.
        Note: It should be specified until when the evaluation was done."""
        for key, value in lst:
            self._add_value(key, value)
        self.evaluated_until = eval_end

    def compute_values(self, end=None):
        """Compute the values inside the interval [0, end].
        Standard value of end is the server budget."""
        # preparation
        hp_period_wcet = [[server.period, server.budget] for server in self.hp_servers]
        if end is None:
            end = self.server.budget

        assert end >= 0

        # case highest priority server
        if len(hp_period_wcet) == 0:
            # no anchor values!
            pass
        else:
            # local variables
            c_prev = 0
            c = 0
            d = 0
            e = 0
            tda_val = 0
            tda_val_prev = 0

            # breakpoint()

            while c <= end:
                # compute by TDA
                tda_val = tda_with_carry_in(hp_period_wcet, c, start_val=tda_val_prev)

                # add value
                d = tda_val - (tda_val_prev + (c - c_prev))
                self._add_value(c, d)

                # find next entry point (where TDA changes)
                e = min([-(tda_val + period - wcet) % period for period, wcet in hp_period_wcet])
                # breakpoint()
                assert e != 0  # This should not be possible

                # # DEBUG
                # print('tda_val', tda_val)
                # print('c', c)
                # print('d', d)
                # print('c_prev', c_prev)
                # print('d_prev', d_prev)

                # update values
                c_prev = c
                tda_val_prev = tda_val
                c = c + e

        self.evaluated_until = end  # update evaluation end


class Rplus(Rplusminus):
    """R^+ function from our paper."""

    def eval(self, x):
        """Evaluate R^+ function value at point x."""
        assert self.evaluated_until >= x
        return x + sum(item for key, item in self.values.items() if x >= key)


class Rminus(Rplusminus):
    """R^- function from our paper."""

    def eval(self, x):
        assert self.evaluated_until >= x
        """Evaluate R^- function value at point x."""
        return x + sum(item for key, item in self.values.items() if x > key)


def tda_with_carry_in(hp_period_wcet, wcet_this, stop_cond=None, start_val=0):
    """Compute WCRT using TDA with carry in.
    hp_period_wcet = list of (period, wcet)-tuples from higher priority tasks
    wcet_this = WCET of the task under analysis

    Notes:
        - blockfct = math.ceil is the standard TDA function
        - blockfct = math.floor +1 is what we utilize here
    """

    # blockfct = math.ceil  # standard way
    blockfct = lambda x: math.floor(x) + 1

    def blocked(interval_length, period, wcet):
        return blockfct((interval_length + period - wcet) / period) * wcet

    t = start_val
    while True:
        val = wcet_this + sum(blocked(t, period, wcet) for period, wcet in hp_period_wcet)
        # print(t, val, sum(blocked(t, period, wcet) for period, wcet in hp_period_wcet))  # debug
        if val <= t:
            assert val == t  # need exact TDA result for computation of Rplus and Rminus
            # if val != t:
            #     print('Note: val != t')
            return t
        if stop_cond is not None and val > stop_cond:
            raise ValueError('A response time under this setting could not be derived', hp_period_wcet, wcet_this,
                             stop_cond, start_val)
        t = val


def wcrt_analysis_single(hp_servers, server, task):
    """Our WCRT analysis for one server.
    (Theorem 4 of our paper)"""
    # Make sure the assumptions are met
    assert task.wcet <= server.budget
    assert task.min_iat >= server.period

    # Define Rplus and Rminus
    rplus = Rplus(hp_servers, server)
    rminus = Rminus(hp_servers, server)

    # Compute anchor values (for fast computation)
    rplus.compute_values()
    rminus.add_values(rplus.values.items(), rplus.evaluated_until)

    # Compute our WCRT bound
    c_values = list(rplus.values)
    c_values += [task.wcet - entry for entry in c_values]  # add inverse C-values
    c_values += [0, task.wcet]  # add outer points.
    c_values.sort()  # sort
    # find values between two values:
    c_middle = [(entry1 + entry2) / 2 for entry1, entry2 in zip(c_values[:-1], c_values[1:])]
    # check all values
    supR = max([rplus.eval(x) + rminus.eval(task.wcet - x) for x in c_middle if 0 <= x < task.wcet])
    res = max(
        server.period - task.min_iat + supR,
        rminus.eval(task.wcet)
    )
    return res


def wcrt_analysis(system):
    """Our WCRT analaysis.
    Input: System()
    Output: A list with all wcrt values for the tasks. """
    res = []
    for idx in range(len(system.servers)):
        res.append(wcrt_analysis_single(system.servers[:idx], system.servers[idx], system.tasks[idx]))
    return res


if __name__ == '__main__':
    """Some testing"""
    # tests = range(20)
    tests = [4]

    if 1 in tests:
        # Test 1: TDA function
        print('===TEST 1===')
        print(tda_with_carry_in([], 5), 'should be 5')
        print(tda_with_carry_in([[10, 1]], 5), 'should be 7')
        print(tda_with_carry_in([[2, 1]], 5), 'should be 12')
        print(tda_with_carry_in([[10, 1], [5, 2]], 5), 'should be 16')
        print(tda_with_carry_in([[10, 1], [5, 2]], 6), 'should be 19')
        print(tda_with_carry_in([[10, 1], [5, 2]], 8), 'should be 24')

    if 2 in tests:
        # Test 2: Another Rplusminus computation
        # make TDA test function:
        print('MANUALLY: TDA Test function')
        for i in range(25):
            print(i, tda_with_carry_in([[10, 1], [5, 2]], i))

        print('MANUALLY: Anchor points:')
        anchors = dict()
        comp = -1
        for i in range(25):
            res = tda_with_carry_in([[10, 1], [5, 2]], i)
            if res != comp + 1:
                print(i, res)
                anchors[i] = res
            comp = res
        print('anchor values from TDA', anchors)

        # obtain the same values by definition through servers
        import benchmark

        server1 = benchmark.Server(10, 1)
        server2 = benchmark.Server(5, 2)
        server3 = None
        Rtest = Rplus([server1, server2], server3)
        Rtest.compute_values(end=25)
        print('anchor increments', Rtest.values)
        print('anchor values from servers', [[x, Rtest.eval(x)] for x in Rtest.values])

        Rtestminus = Rminus([server1, server2], server3)
        Rtestminus.add_values(Rtest.values.items(), Rtest.evaluated_until)  # hand over values
        print([[x, Rtestminus.eval(x)] for x in Rtestminus.values])

    if 3 in tests:
        # Test 3: Rplusminus computation
        import benchmark

        server1 = benchmark.Server(10, 1)
        server2 = benchmark.Server(5, 1)
        server3 = None
        Rtest = Rplus([server1, server2], server3)
        Rtest.compute_values(end=25)
        print('anchor increments', Rtest.values)
        print('anchor values from servers', [[x, Rtest.eval(x)] for x in Rtest.values])

        Rtestminus = Rminus([server1, server2], server3)
        Rtestminus.add_values(Rtest.values.items(), Rtest.evaluated_until)  # hand over values
        print([[x, Rtestminus.eval(x)] for x in Rtestminus.values])

    if 4 in tests:
        # Test 4: Case Study
        import benchmark

        server1 = benchmark.Server(10, 2)
        server2 = benchmark.Server(20, 4)
        server3 = benchmark.Server(50, 10)
        server4 = benchmark.Server(100, 10)

        task1 = benchmark.Task(12, 1)
        task2 = benchmark.Task(20, 4)
        task3 = benchmark.Task(60, 8)
        task4 = benchmark.Task(130, 9)

        system = benchmark.System(
            [server1, server2, server3, server4],
            [task1, task2, task3, task4]
        )

        print(wcrt_analysis(system))
