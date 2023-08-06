class Job:

    """
        A job captures all information about an AGVs current task.

        Parameters
        ----------
        type : int
            type of the job
            0: 'idle',
            1: 'charge',
            2: 'reposition',
            3: 'preprocess',
            4: 'serve'

        origin : [int, int]
            origin coordinates of the job
        dest : [int, int]
            destination coordinatess of the job

        Returns
        -------
        An object of Job class
    """

    def __init__(self, env, id, type, origin, dest):
        self.id = id
        self.job_dict = {
            0: 'idle',
            1: 'charge',
            2: 'reposition',
            3: 'preprocess',
            4: 'serve'
        }
        self.elapsed_time = 0
        self.type = type
        self.origin = origin
        self.dest = dest
        if self.type in [2, 3, 4]:
            self.path = env.maze.solve(self.origin, self.dest)[0]
        self.completed = False

    def __repr__(self):
        return f'[Id:{self.id}, elapsed time:{self.elapsed_time}, type:{self.type}, (O,D):{(self.origin, self.dest)}]'

    def check_completion(self, coordinates):
        if coordinates == self.dest:
            self.completed = True
