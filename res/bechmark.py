"""Synthetic creation of servers and tasks."""


class System:
    """One system that has to be analysed."""

    def __init__(self, servers, tasks):
        # check if length matches
        assert len(servers) == len(tasks)
        self.servers = servers
        self.tasks = tasks

    def server_task_tuples(self):
        return zip(self.servers, self.tasks)

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

    @staticmethod
    def help():
        print('Server(<replenishment period>, <budget of the server>')
        print('var: period, budget')


class Task:
    """A tasks."""

    def __init__(self, minimum_inter_arrival_time, wcet):
        self.min_iat = minimum_inter_arrival_time
        self.wcet = wcet

    @staticmethod
    def help():
        print('Task(<minimum inter arrival time>, <worst case execution time>')
        print('var: min_iat, wcet')


'''reference: from https://github.com/tu-dortmund-ls12-rt/SSSEvaluation'''
