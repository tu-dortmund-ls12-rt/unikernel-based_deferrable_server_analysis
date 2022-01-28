"""RTC based analysis from Cuijpers and Bril in 2007."""


def wcrt_analysis_single(server, task):
    res = task.wcet * server.period / server.budget + 2 * server.period
    assert task.min_iat + 2 * server.period >= res
    return task.wcet * server.period / server.budget + 2 * server.period


def wcrt_analysis(system):
    return [wcrt_analysis_single(server, task) for server, task in system.server_task_tuples()]


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
