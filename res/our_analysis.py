"""Our analysis."""
import math


class Rplusminus:
    """Parent class for Rplus and Rminus"""

    def __init__(self):
        self.values = dict()
        pass

    def add_value(self, key, value):
        """Add one more key and value to the list."""
        assert key not in self.values
        self.values[key] = value

    def add_values(self, lst):
        """Add several keys and values to the list all at once."""
        for key, value in lst:
            self.add_value(key, value)


class Rplus(Rplusminus):
    """R^+ function from our paper."""

    def compute(self, x):
        """Compute R^+ function value at point x."""
        return x + sum(item for key, item in self.values.items() if x >= key)


class Rminus(Rplusminus):
    """R^- function from our paper."""

    def compute(self, x):
        """Compute R^- function value at point x."""
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
        print(t, val, sum(blocked(t, period, wcet) for period, wcet in hp_period_wcet))  # debug
        if val <= t:
            assert val == t  # need exact TDA result for computation of Rplus and Rminus
            # if val != t:
            #     print('Note: val != t')
            return t
        if stop_cond is not None and val > stop_cond:
            raise ValueError('A response time under this setting could not be derived', hp_period_wcet, wcet_this,
                             stop_cond, start_val)
        t = val


if __name__ == '__main__':
    """Some testing"""

    # Test 1:
    print('===TEST 1===')
    print(tda_with_carry_in([], 5), 'should be 5')
    print(tda_with_carry_in([[10, 1]], 5), 'should be 7')
    print(tda_with_carry_in([[2, 1]], 5), 'should be 12')
    print(tda_with_carry_in([[10, 1], [5, 2]], 5), 'should be 16')
    print(tda_with_carry_in([[10, 1], [5, 2]], 6), 'should be 19')
    print(tda_with_carry_in([[10, 1], [5, 2]], 8), 'should be 24')
