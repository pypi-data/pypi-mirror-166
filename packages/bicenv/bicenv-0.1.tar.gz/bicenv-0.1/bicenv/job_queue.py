from .job import Job


class JobQueue:

    """
        A Job Queuing data structure.

        Parameters
        ----------
        None

        Returns
        -------
        an object of Job Queue class.
        """

    def __init__(self):
        self.jobs = [None, None, None]
        self.queue_capacity = len(self.jobs)

    def __repr__(self):
        return f'{self.jobs}'

    def reset(self, env):
        self.jobs = [None, None, None]
        self.set_job(env, None, 0, 0, (0, 0), (0, 0))

    def left_shift(self):
        self.jobs = self.jobs[1:] + [None]

    def get_preemptable_job_index(self):
        for i, job in enumerate(self.jobs):
            if job == None:
                return i
            elif job.type in [0, 1, 2]: #because 3:preprocess and 4:serve are non-preemtable
                return i
            else:
                continue
        return 5

    def has_space_for_new_assignment_request(self):
        """Returns true if a new transport request can be placed in the job queue of the AGV

        Returns
        -------
        [Boolean]
            [true if a new request can be placed in the job queue of the AGV, False otherwise]
        """
        return self.get_preemptable_job_index() + 1 < self.queue_capacity


    def has_space_for_new_reposition_request(self):
        """Returns true if a new reposition request can be placed in the job queue of the AGV

        Returns
        -------
        [Boolean]
            [true if a new request can be placed in the job queue of the AGV, False otherwise]
        """
        return self.get_preemptable_job_index() < self.queue_capacity

    def get_job(self, i):
        """
        Index a job of the queue by the job number.

        Parameters
        ----------
        i : int
            index of the job

        Returns
        -------
        an object of Job class.
        """
        return self.jobs[i]

    def set_job(self, env, id, i, job, origin, dest):
        """
        self, latest_request.id, job_idx + 1, 4, latest_request.origin,latest_request.dest
        Set a job of the queue by the job number.

        Parameters
        ----------
        i : int
            index of the job
        job : int
            type of Job
        Returns
        -------
        an object of Job class.
        """
        self.jobs[i] = Job(env, id, job, origin, dest)
