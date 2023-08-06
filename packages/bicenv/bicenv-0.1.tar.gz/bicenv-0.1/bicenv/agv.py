from .job_queue import JobQueue
import functools

class AGV:

    """
    AGV.

    Parameters
    ----------
    id: int
        identification number of AGV
    velocity : int
        velocity of AGV in meters per second
    max_charge : float
        maximum charge capacity of AGV
    discharging_rate: float
        discharging rate of AGV
    charging_rate: float
        charging rate of AGV
    init_x : int
        initial X coordinate of AGV
    init_y : int
        initial Y coordinate of AGV

    Returns
    -------
    an object of AGV class
    """

    def __init__(
        self,
        id,
        type,
        velocity,
        max_charge,
        discharging_rate,
        charging_rate,
        critical_charge_level,
        capabilities,
        travel_time_cost,
        init_x,
        init_y,
    ):
        self.obj_type = "agv"
        self.id: int = id
        self.type:str = type
        self.velocity: int = velocity
        self.max_charge: float = max_charge
        self.charge: float = self.max_charge
        self.charging_rate: float = charging_rate
        self.discharging_rate: float = discharging_rate
        self.critical_charge_level: float = critical_charge_level
        self.capabilities: str = capabilities
        self.x: int = init_x
        self.y: int = init_y
        self.job_queue = JobQueue()
        self.distance_buffer = 0
        self.eta = 0
        self.eca = 100
        self.travel_cost = travel_time_cost # travel_time_cost cent per second
        self.travel_time_since_last_step:float = 0.0
        # Stats
        self.loaded_travel = 0
        self.unloaded_travel = 0
        self.requests_served = 0

    def reset(self, *args, **kwargs):
        self.obj_type = "agv"
        self.x: int = kwargs.get('x')
        self.y: int = kwargs.get('y')
        self.charge = kwargs.get('charge')
        self.job_queue = JobQueue()
        self.distance_buffer = 0
        self.eta = 0
        self.eca = self.charge
        self.travel_time_since_last_step:float = 0.0
        # Stats
        self.loaded_travel_time = 0
        self.unloaded_travel_time = 0
        self.requests_served = 0

    def get_time(self, env, directions):
        dist = 0
        for direction in directions:
            if direction in [1, 3, 5, 7]:
                scaled_dist = env.d_dist
            elif direction in [0, 2, 4, 6]:
                scaled_dist = env.s_dist
            dist += scaled_dist

        
        time = dist/self.velocity
        # To reduce error in estimations
        return round(time/env.increment_epoch) * env.increment_epoch

    def set_eta_and_eca(self, env):
        """
        Set Expected duration after which non pre-emptable jobs are finished (eta - expected time till availability)
        Set Expected charge level of the AGV when it finishes all its non-preemptable jobs (eca - expected charge at availability)
        """

        self.eta = 0
        self.eca = self.charge

        preemptable_job_index = self.job_queue.get_preemptable_job_index()
        if preemptable_job_index == 0:
            self.eta = 0
            self.eca = self.charge

        elif preemptable_job_index == 5:
            total_path = []
            path, _ = env.maze.solve((self.x, self.y), self.job_queue.jobs[0].dest)
            total_path += path
            for j in range(1, 3):
                path, _ = env.maze.solve(
                    self.job_queue.jobs[j].origin, self.job_queue.jobs[j].dest
                )
                total_path += path
            self.eta = self.get_time(env, total_path)
            self.eca = self.charge - (self.eta * self.discharging_rate)
            return
        else:
            total_path = []
            path, _ = env.maze.solve((self.x, self.y), self.job_queue.jobs[0].dest)
            total_path += path
            for j in range(1, preemptable_job_index):
                path, _ = env.maze.solve(
                    self.job_queue.jobs[j].origin, self.job_queue.jobs[j].dest
                )
                total_path += path
            self.eta = self.get_time(env, total_path)
            self.eca = self.charge - (self.eta * self.discharging_rate)

    def _is_capable_for_assignment(self, request):
        '''
        This function checks if the agv has required capabilities to do the task
        '''
        caps_to_check = request.capability_requirements.split(',')

        b = [str(c) in self.capabilities for c in caps_to_check]
        # reduce does pairwise comparison of 2 objects in a list
        return functools.reduce(lambda x, y: x and y, b)


    def is_eligible_for_assignment(self, request=None, env=None, check_eca=False):
        """Checks if the AGV is eligible

        Parameters
        ----------
        request : [Request], optional
            [To use the request for checking], by default None
        env : [Environment], optional
            [Environment], by default None
        check_eca : bool, optional
            [Check Expected charge when available rather than current charge], by default False

        Returns
        -------
        [bool]
            [True if eligible, false otherwise]
        """
        if request is None:
            if self.job_queue.has_space_for_new_assignment_request():  # AGV has enough space for a transport request
                if check_eca:
                    self.set_eta_and_eca(env)
                    if self.eca >= self.critical_charge_level:
                        return True
                    else:
                        return False

                if (
                    self.charge >= self.critical_charge_level
                ):  # AGV has sufficient charge
                    return True
                else:
                    return False
            else:
                return False

        else:
            if self._is_capable_for_assignment(request):
                if self.job_queue.has_space_for_new_assignment_request():  # AGV has enough space for a transport request
                    if check_eca:
                       self.set_eta_and_eca(env)
                       if self.eca >= self.critical_charge_level:
                           return True
                       else:
                           return False

                    if (self.charge >= self.critical_charge_level):  # AGV has sufficient charge
                        return True
                    else:
                        return False

                else:
                    return False
            else:
                return False


    def is_eligible_for_reposition(self, env=None):
        """Checks if the AGV is eligible

        Parameters
        ----------
        request : [Request], optional
            [To use the request for checking], by default None
        env : [Environment], optional
            [Environment], by default None
        check_eca : bool, optional
            [Check Expected charge when available rather than current charge], by default False

        Returns
        -------
        [bool]
            [True if eligible, false otherwise]
        """
        
        if self.job_queue.has_space_for_new_reposition_request():  # AGV has enough space for a reposition request
            self_loc = (self.x, self.y)
            if self_loc in env.stations:
                if (self.charge >= self.critical_charge_level):  # AGV has sufficient charge
                    return True
                else:
                    return False
            elif (self_loc not in env.stations) and (self.charge < self.critical_charge_level) and (self.get_current_job() is not None) and (self.get_current_job().type == 2):
                # print(f'AGV:{self} was already repositioning with low battery when a new repositioing was requested')
                return False
            else:
                return True  # if the agv does not have sufficient charge but it is not at the charging station, which means it is probably repositioning, then it is eligible      
        return False
        

    def get_exp_wait_and_serve_time(self, env, request):
        """Return the expected time that the request will have to wait before being picked up, and the serve time
        Parameters
        ----------
        env : [Environment]

        request : [Request]
            [Request to be picked up]

        Returns
        -------
        [Float]
            [Waiting time, serve time]
        """

        waiting_time = 0.0
        total_path = []

        for job in self.job_queue.jobs:
            if job is None:
                continue
            if job.type == 0:  # idle
                continue
            if job.type == 1:  # Charge
                if self.charge < self.critical_charge_level:
                    time_to_charge_until_ct = (
                        self.critical_charge_level - self.charge
                    ) / self.charging_rate
                    waiting_time += time_to_charge_until_ct
                continue
            if job.type == 2:  # Reposition
                path, _ = env.maze.solve(job.origin, job.dest)
                total_path += path
                continue
            if job.type == 3:  # Preprocess
                assert (
                    job.id == request.id
                ), "Job's id does not match active request's id"
                path, _ = env.maze.solve(job.origin, job.dest)
                total_path += path
                continue
            if job.type == 4:  # Serve and non-preemptable
                if job.id != request.id:
                    path, _ = env.maze.solve(
                        (self.x, self.y), job.dest
                    )  # because the AGV is serving a request and may not be at job's origin
                    total_path += path
                else:
                    assert (
                        job.id == request.id
                    ), "Job's id does not match active request's id"
                    serve_path, _ = env.maze.solve(job.origin, job.dest)
                continue

        waiting_time += self.get_time(env, total_path)
        serve_time = self.get_time(env, serve_path)
        return waiting_time, serve_time

    def __repr__(self):
        """
        Object representation in readable format
        """
        return f"AGV_{self.id}, charge:{self.charge}, (x,y):{(self.x, self.y)}, current job Q:{self.job_queue}"

    def reposition_agv(self, env):
        def get_extra_distance(env, total_distance, directions):
            dist = 0
            for direction in directions:
                if direction in [1, 3, 5, 7]:
                    scaled_dist = env.d_dist
                elif direction in [0, 2, 4, 6]:
                    scaled_dist = env.s_dist
                dist += scaled_dist
            return total_distance - dist

        current_job = self.job_queue.get_job(0)
        path = current_job.path

        # To Solve the error in distance calculation
        if len(path) <= 0 and current_job.completed == False:
            # print(f'Recalculate Path for {self} at day: {env.now_day()}, time: {env.now_time()}')
            current_job.path, _ = env.maze.solve((self.x, self.y), current_job.dest)
            path = current_job.path

        if not len(path) == 0:
            epoch = env.increment_epoch
            velocity = self.velocity
            total_distance = (velocity * epoch) + self.distance_buffer
            acc_dist = 0
            for i, direction in enumerate(path):
                j = i
                if acc_dist > total_distance:
                    j -= 1
                    break
                if direction in [1, 3, 5, 7]:
                    scaled_dist = env.d_dist
                elif direction in [0, 2, 4, 6]:
                    scaled_dist = env.s_dist
                acc_dist += scaled_dist
            processed_dir = path[: j + 1]
            rem_directions = path[j + 1 :]
            self.distance_buffer = get_extra_distance(
                env, total_distance, processed_dir
            )
            current_job.path = rem_directions

            for dir in processed_dir:
                # 0 N, 1 NE, 2 E, 3 SE, 4 S, 5 SW, 6 W, 7 NW
                if dir == 0:
                    self.y -= 1
                if dir == 1:
                    self.x += 1
                    self.y -= 1
                if dir == 2:
                    self.x += 1
                if dir == 3:
                    self.x += 1
                    self.y += 1
                if dir == 4:
                    self.y += 1
                if dir == 5:
                    self.x -= 1
                    self.y += 1
                if dir == 6:
                    self.x -= 1
                if dir == 7:
                    self.x -= 1
                    self.y -= 1
            self.x = min(self.x, env.x_range - 1)
            self.y = min(self.y, env.y_range - 1)
            self.x = max(self.x, 0)
            self.y = max(self.y, 0)

    def execute_job(self, env):
        # this is a constant to record how much agv state changes in each increment step
        time = env.increment_epoch
        current_job = self.job_queue.get_job(0)
        if current_job == None:
            if (self.x, self.y) in env.stations:
                if self.charge == self.max_charge:
                    # params: env, id, i, jobType, origin, dest
                    self.job_queue.set_job(env, None, 0, 0, (0, 0), (0, 0))
                elif self.charge < self.max_charge:
                    self.job_queue.set_job(env, None, 0, 1, (0, 0), (0, 0))
        if current_job.type == 0:  # idle
            # self.charge = min(0, self.charge - (self.discharging_rate * time))
            pass
        elif current_job.type == 1:  # charge
            self.charge = min(
                self.max_charge, self.charge + (self.charging_rate * time)
            )

        elif current_job.type == 2:  # reposition
            #TODO: Check this
            if current_job.origin == current_job.dest:
                self.charge = min(
                    self.max_charge, self.charge + (self.charging_rate * time)
                )
            else:
                self.record_agv_travel(time, loaded=False)
                # Check whether AGV still has charge before incrementing its coordinates
                if self.charge > 0:
                    self.reposition_agv(env)
                    self.charge = max(0, self.charge - (self.discharging_rate * time))
                else:
                    print(self)
                    raise RuntimeError(f"AGV:{self} has 0% Charge at day: {env.now_day()}, time: {env.now_time()}")

        elif current_job.type == 3 or current_job.type == 4:  # preprocess, serve

            if current_job.type == 3:
                self.record_agv_travel(time, current_job, env, loaded=False)
            if current_job.type == 4:
                self.record_agv_travel(time, current_job, env, loaded=True)
            # Check whether AGV still has charge before incrementing its coordinates
            if self.charge > 0:
                self.reposition_agv(env)
                self.charge = max(0, self.charge - (self.discharging_rate * time))
            else:
                print(self)
                raise RuntimeError(f"AGV:{self} has 0% Charge at day: {env.now_day()}, time: {env.now_time()}")
                
        current_job.check_completion((self.x, self.y))

        # left shifting job queue if job completed
        if current_job.completed:
            self.job_queue.left_shift()
            if current_job.type == 4:  # Serve
                # print(f"Finished Serve for {current_job}")
                self.requests_served += 1
                return True, current_job.id
            if current_job.type == 3:  # Preprocess
                # print(f"Finished Preprocess for {current_job}")
                env.record_req_pickup(current_job.id)

        current_job.elapsed_time += time
        return False, None

    def record_agv_travel(self, time, current_job=None, env=None, loaded=False):
        
        self._increment_travel_time_since_last_step(time)

        if loaded:
            self.loaded_travel_time += time
        else:
            self.unloaded_travel_time += time


    def get_current_job(self):
        """Returns the current job that the AGV is doing

        Returns
        -------
        [Job]
            [The Job that the AGV is doing]
        """
        current_job = self.job_queue.get_job(0)
        return current_job


    def _get_travel_time_since_last_step(self):
        return self.travel_time_since_last_step

    def _increment_travel_time_since_last_step(self, time):
        self.travel_time_since_last_step += time

    def _reset_travel_time_since_last_step(self):
        """Resets travel time counter
        """
        self.travel_time_since_last_step = 0.0
