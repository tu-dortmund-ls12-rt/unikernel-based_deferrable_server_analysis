"""State of the art (RTC based) analysis from Cuijpers and Bril in 2007."""
from our_analysis import Rminus


def wcrt_analysis_single_pessimistic(server, task):
    res = task.wcet * server.period / server.budget + 2 * server.period
    assert task.min_iat + 2 * server.period >= res
    return task.wcet * server.period / server.budget + 2 * server.period


def wcrt_analysis_single(hp_servers, server, task):
    # compute Rminus
    rminus = Rminus(hp_servers, server)
    rminus.compute_values()

    # result
    res = task.wcet * server.period / server.budget + 2 * rminus.eval(server.budget)

    assert task.min_iat + 2 * server.period >= res
    assert task.wcet * server.period / server.budget + 2 * server.period >= res

    return res


def wcrt_analysis(system):
    res = []
    for idx in range(len(system.servers)):
        res.append(wcrt_analysis_single(system.servers[:idx], system.servers[idx], system.tasks[idx]))
    return res


if __name__ == '__main__':
    """Some testing."""

    tests = range(20)
    # tests = [4]

    if 1 in tests:
        # Test 1: Case Study
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
