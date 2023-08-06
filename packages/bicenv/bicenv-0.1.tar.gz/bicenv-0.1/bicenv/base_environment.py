from ast import Raise
import typing
from typing import Tuple, Any, List
from urllib import request
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np
import pandas as pd
import json
import math
import random
from gym import Env
from .station import Station
import time
from .stats import Statistics
from .agv import AGV
from .pdnode import PDNode
from .parent_area import Parent
from .request import Request
from .path_finding import Maze



class Environment(Env):

    """
    A simulated model of a defined system of order dispatching with AGVs.

    Parameters
    ----------
    config: JSON
        path to configuration JSON file

    Returns
    -------
    an object of Environment class
    """

    def __init__(self, config, *args, **kwargs):
        self.is_debug_enabled = False
        

        self.debug("Compiling environment, please wait.")
        self.policy_type = kwargs.get('policy_type', None)
        self.temp = {}  # To Hold Temporary data that doesnt change
        

        # Open the main Config file
        with open(config, "r") as f:
            config = json.load(f)
            f.close()

        # Open environment configuration file
        with open(config["env_config_file"], "r") as f:
            config_env = json.load(f)
            f.close()

        # Open layout configuration file
        with open(config["layout_config_file"], "r") as f:
            config_layout = json.load(f)
            f.close()

        # Open AGVs configuration file
        with open(config["agv_config_file"], "r") as f:
            config_agvs = json.load(f)
            f.close()

        # Open Requests configuration file
        with open(config["request_config_file"], "r") as f:
            config_requests = json.load(f)
            f.close()

        # Open time window configuration file
        with open(config["tw_config_file"], "r") as f:
            config_tw = json.load(f)
            f.close()

        # reward & costs init
        self.reward = 0.0
        self.request_tardiness_costs = []
        self.assignee_agv_travel_costs = []

        self.R1 = False # R1: EXP_TARDINESS_AND_EXP_ASSIGNED_AGV_COSTS
        self.R2 = False  # R2: R_TARDINESS_AND_R_ASSIGNED_AGV_COSTS
        self.R3 = False # R3: EXP_TARDINESS_AND_EXP_ASSIGNED_AGV_COSTS_AND_R_FLEET_TRAVEL_COSTS
        self.R4 = False # R4: R_TARDINESS_AND_R_ASSIGNED_AGV_COSTS_AND_R_FLEET_TRAVEL_COSTS
        self.R5 = False # R5: R_TARDINESS_AND_R_FLEET_TRAVEL_COSTS
        self.R6 = False # R6: EXP_TARDINESS_AND_R_FLEET_TRAVEL_COSTS
        self.R7 = False # R7: From paper 3

        reward_structure = config_env["reward_structure"]
        setattr(self, reward_structure, True)

        # Should the training episode end after the agent takes infeasible action
        self.terminate_on_infeasible_action: bool = config_env[
            "terminate_on_infeasible_action"
        ]

        # Request Configs
        # Create requests from
        self.request_from = config_layout["request_from"]
        # Capabilities to sample
        self.capability_requirements = config_requests["capability_requirements"]
        # Request costs to assign
        self.request_costs = config_requests["request_costs"]
        # Inflation factor to adjust itme window tightness
        self.inflation_factor = config_tw["inflation_factor"]
        # TODO: Either remove or make permanent
        self.use_one_hot_encoded_locs = True
        # Should the agent mask infeasible actions
        self.mask_infeasible_actions: bool = config_env["mask_infeasible_actions"]
        # Infeasible action penalty
        self.infeasible_assignment_reward_multiplier = config_env["infeasible_assignment_reward_multiplier"]
        # Infeasible reposition action penalty
        self.infeasible_reposition_reward_multiplier = config_env["infeasible_reposition_reward_multiplier"]
        # reward for rejecting a request
        self.request_rejection_reward_multiplier = config_env["request_rejection_reward_multiplier"]
        # the amount of time in seconds that progresses after each call in simulation
        self.increment_epoch: int = config_env["increment_epoch"]
        # length of the environment (X axis) in meters
        self.length = config_layout["length"]
        # width of the environment (Y axis) in meters
        self.width = config_layout["width"]
        # calculate max-dist in the layout
        self.max_dist = (self.length ** 2 + self.width ** 2) ** (1 / 2)
        # space discretization parameter, creates the grid a size of d_g x d_g
        self.d_g: float = config_env["d_g"]
        # straight distance of a cell
        self.s_dist: float = self.d_g
        # diagonal distance of a cell
        self.d_dist: float = (2 * self.d_g ** 2) ** (1 / 2)
        # computes the number of cells to make in x direction
        self.x_range = math.ceil(self.length / self.d_g)
        # compute number of cells to make in y direction
        self.y_range = math.ceil(self.width / self.d_g)

        self.info = {
            "time": 0,
            "day": 0,
        }
        self.invoked_by_new_req = False

        self.figure, self.ax = None, None

        self.RENDER_PAUSE = 0.05

        # Create Parents and their children (Departments and machines, for example)

        pd_parents = config_layout["parents"]["PD"]

        self.parents = []
        for parent in pd_parents:
            # parent_id, x, y, width, length, arrival_rate (jobs/hour), is_temporal, days_active, start_times, durations
            (
                p_id,
                p_x,
                p_y,
                p_length,
                p_width,
                p_arrival_rate,
                is_temporal,
                active_days,
                start_times,
                durations,
                parent_type
            ) = parent
            parent_obj = Parent(
                parent_id=p_id,
                x=p_x // self.d_g,
                y=p_y // self.d_g,
                width=p_width // self.d_g,
                length=p_length // self.d_g,
                arrival_rate=(p_arrival_rate * self.increment_epoch) / 3600,
                is_temporal=is_temporal,
                active_days=active_days,
                start_times=start_times,
                durations=durations,
                parent_type=parent_type,
            )
            children_locs = config_layout["children"]["PD"][str(p_id)]
            parent_obj.loc_children = children_locs
            parent_obj.loc_children = [
                (element[0] // self.d_g, element[1] // self.d_g)
                for element in parent_obj.loc_children
            ]
            parent_obj.num_children = len(children_locs)
            self.info[f"P{p_id}"] = parent_obj
            self.parents.append(parent_obj)
        
        # Get max distance from each parent
        self.max_dist_parent = max([d.get_max_dist() for d in self.parents])
        # Create Charging Stations and add to Info
        self.stations = []
        # 1 is hardcoded for now since all charging stations are homogeneous
        stations = config_layout["children"]["S"]["1"]
        for n, station in enumerate(stations):
            x = station[0] // self.d_g
            y = station[1] // self.d_g
            station_obj = Station(x, y)
            self.info[f"C{n+1}"] = station_obj
            self.stations.append((x, y))
        self.n_stations = n + 1

        # Create AGVs and add to Info
        
        agv_types = config_agvs.keys()
        agv_idx = 0

        self.agvs = []

        for agv_type in agv_types:
            agv_type_config = config_agvs[agv_type]
            velocity = agv_type_config['velocity']
            max_charge = agv_type_config['max_charge']
            charging_rate = agv_type_config['charging_rate']
            discharging_rate = agv_type_config['discharging_rate']
            critical_charge_level = agv_type_config['critical_charge_level']
            capabilities = agv_type_config['capabilities']
            travel_time_cost = agv_type_config['travel_time_cost']
            quantity = agv_type_config['quantity']
            for i in range(quantity):
                agv_idx += 1
                agv_obj = AGV(
                id = agv_idx,
                type = agv_type,
                velocity = velocity,
                max_charge = max_charge,
                discharging_rate = discharging_rate,
                charging_rate = charging_rate,
                critical_charge_level = critical_charge_level,
                capabilities = capabilities,
                travel_time_cost = travel_time_cost,
                init_x = 0,
                init_y = 0,)

                self.agvs.append(agv_obj)
                self.info[f"V{agv_idx}"] = agv_obj

        
        self.n_AGVs = agv_idx

        # Min AGV Speed

        self.min_agv_speed = min([agv.velocity for agv in self.agvs])

        # Path Finding
        self.grid = np.zeros([self.x_range, self.y_range])  # grid representation
        self.req_id = 0  # to keep track of requests that arrive over time
        self.new_req = False
        self.complete_req = False
        self.maze = Maze(self.grid, config)

        # Create Blocked Cells
        self.blocked_cells = []
        for n, block in enumerate(config_layout["Blocked"]):
            self.blocked_cells.append((block[0] // self.d_g, block[1] // self.d_g))

        # Create Taxi Zones
        self.tz_d = config_env["taxi_zone_size"]
        self.taxi_zones = {}
        self.divisions = []
        self.debug("Setting Taxi Zone ranges now.")
        for y in range(0, self.y_range, self.tz_d):
            for x in range(0, self.x_range, self.tz_d):
                self.divisions.append([(x, x + self.tz_d), (y, y + self.tz_d)])
        self.debug("Dividing the geographical space into taxi zones now.")
        for i, zone_ranges in enumerate(self.divisions):
            for y in range(zone_ranges[1][0], zone_ranges[1][1]):
                for x in range(zone_ranges[0][0], zone_ranges[0][1]):
                    self.taxi_zones[(x, y)] = i + 1
        self.n_taxi_zones = len(self.divisions)
        self.closest_stations = {}
        self.debug("Determining closest Charging Stations now.")
        self.temp["tz_centers"] = []

        for tz in range(len(self.divisions)):
            tz_center = (
                (self.divisions[tz][0][0] + self.divisions[tz][0][1]) // 2,
                (self.divisions[tz][1][0] + self.divisions[tz][1][1]) // 2,
            )
            self.temp["tz_centers"].append(tz_center)
            closest_station = None
            closest_distance = float("inf")
            for station in self.stations:
                # print(self.taxi_zones[tz], station)
                # path, _ = self.maze.solve(tz_center, station)
                # print("TZ CENTER:", tz_center, "STATION:", station)
                path = self._get_euclidean_distance(tz_center[0], tz_center[1], station[0], station[1])

                if path <= closest_distance:
                    closest_distance = path
                    closest_station = station
            # print(closest_station, closest_distance)
            self.closest_stations[tz + 1] = closest_station
        self.agg_days = 0
        # Simulation horizon length
        self.horizon = config_env["horizon"]
        
        # For Statistics
        self.stats = Statistics("temp", "run")

        # Hold Temporary data that doesnt change such as blocked cells and department and hotspot rectangles
        self.temp["x_ticks"] = list(range(self.x_range))
        self.temp["y_ticks"] = list(range(self.y_range))

        self.temp["blocked_x"] = [blocked[0] for blocked in self.blocked_cells]
        self.temp["blocked_y"] = [blocked[1] for blocked in self.blocked_cells]
        self.temp["children_x"] = []
        self.temp["children_y"] = []
        for parent in self.parents:
            for child_loc in parent.loc_children:
                self.temp["children_x"].append(child_loc[0])
                self.temp["children_y"].append(child_loc[1])
        # Taxi-Zones
        self.temp["tz_colors"] = []
        flag = 0

        for i in range(len(self.divisions)):
            color = (
                ["blue", "white"][flag] if i % 2 == 0 else ["blue", "white"][1 - flag]
            )
            flag = (
                1 - flag
                if (i + 1) % (self.x_range / self.tz_d) == 0 and i > 0
                else flag
            )
            self.temp["tz_colors"].append(color)

        self.temp["stations_in_tz"] = {}

        

        # stores the stations in each taxi zone
        for tz in range(1, self.n_taxi_zones+1):
            stations = self._stations_in_tz(tz)
            if len(stations) > 0:
                self.temp["stations_in_tz"][tz] = stations
            else:
                self.temp["stations_in_tz"][tz] = [self.closest_stations[tz]]

        self.render_toggle = False
        

    def set_policy_type(self, policy_type):
        """Sets the policy type, to generate state representation, and control prgram flow

        Parameters
        ----------
        policy_type : [String]
            [Policy Type "SARL", "MARL", "NONRL"]
        """
        self.policy_type = policy_type

    def change_reward_structure(self, reward_structure):
        """Changes the reward structure of the environment

        Parameters
        ----------
        reward_structure : [String]
            [Reward Structure "linear", "quadratic", "exponential"]
        """
        self.R1, self.R2, self.R3, self.R4, self.R5, self.R6 = False, False, False, False, False, False
        setattr(self, reward_structure, True)
        

    def _stations_in_tz(self, tz):
        """Returns a list of stations in a taxi zone

        Parameters
        ----------
        tz : [Integer]
            [Taxi Zone]

        Returns
        -------
        [List]
            [List of stations in a taxi zone]
        """
        return [
            station
            for station in self.stations
            if self.taxi_zones[station] == tz
        ]


    def get_stations_tz(self, tz):
        """Returns the taxi zone of a station

        Parameters
        ----------
        station : [List]
            [Station]

        Returns
        -------
        [Integer]
            [Taxi Zone]
        """
        return self.temp["stations_in_tz"][tz]


    def reset(self):
        """
        Resets the simulation.

        Parameters
        ----------
        None

        Returns
        -------
        state : (time, request, vehicles)
        """
        charging_station_coor = {}
        i = 0
        to_delete = []
        for element_key, element in self.info.items():
            try:
                if element.obj_type == "station":
                    # initialize x and y locations of stations/charging stations
                    charging_station_coor[i] = (element.x, element.y)
                    i += 1
                # Delete all the requests in the system
                if element.obj_type == "request":
                    to_delete.append(element_key)
            except AttributeError:
                pass
        # Delete all the requests in the system
        for element_key in to_delete:
            del self.info[element_key]

        for element in self.info.values():
            try:
                if element.obj_type == "agv":
                    charging_station_number = np.random.choice(np.arange(i))
                    # initialize AGV initial locations on randomly chosen charging stations
                    element.reset(x = charging_station_coor[charging_station_number][0], \
                        y = charging_station_coor[charging_station_number][1], \
                            charge = np.random.randint(3 * element.critical_charge_level, element.max_charge))

            except AttributeError:
                pass
        self.info["time"] = 0  # reset the time in seconds and day number
        # Pick a random day number between 0 and 6 (Sunday - Saturday)
        self.info["day"] = np.random.randint(0, 7)
        # @stat Reinitialize Stats and Record day number
        self.stats = Statistics("temp", "run")
        self.stats.agg_results["inf_assignment_count"] = 0
        self.stats.agg_results["inf_reposition_count"] = 0
        self.agg_days = 0  # aggregate days to end simulation
        
        # while not self.new_req:  # run till a new request pops up
        #     self.increment()
        state_dict = self.generate_state_dict(new_req_trigger=False)
        self.req_id = 0  # to keep track of requests that arrive over time
        self.new_req = False
        self.invoked_by_new_req = False
        return state_dict  # (time, request, vehicles)

    def sample_action(self):
        '''
        Generate an action by sampling from the action_space
        '''
        return self.action_space.sample()
    
    def increment(self):
        """
        Increments the time in the simulation by one increment epoch.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # self.debug('increment')
        if self.render_toggle:
            self.render()
        completed_req_ids = []
        self.complete_req = False
        for element_key in self.info:
            element = self.info[element_key]
            try:
                if element.obj_type == "agv":
                    compl_req, completed_req_id = element.execute_job(self)
                    if completed_req_id is not None:
                        self.complete_req = compl_req
                        completed_req_ids.append(completed_req_id)
                if element.obj_type == "request":
                    element.elapsed_time += self.increment_epoch
            except AttributeError:
                if element_key == "time":
                    self.info[element_key] += self.increment_epoch
                if self.info["time"] > 60 * 60 * 24:
                    self.info["day"] += 1
                    self.agg_days += 1
                    self.info["time"] = self.info["time"] - 60 * 60 * 24
                if self.info["day"] > 6:
                    self.info["day"] = 0

        # self.debug(self.info['time'])

        # Sample a request from hotspots
        if self.request_from.lower() == 'within_layout':
            origin, dest, ept, ldt, request_cost, capability_requirements = self.create_request_from_layout()

        elif self.request_from.lower() == 'within_parent':
            origin, dest, ept, ldt, request_cost, capability_requirements = self.create_request()
        

        if origin is not None:
            self.info["request_%d" % (self.req_id)] = Request(id=self.req_id, origin=origin, dest=dest, ept=ept, ldt=ldt,  request_cost=request_cost, capability_requirements=capability_requirements)
            self.record_req_arr(self.req_id)  # Record request arrival moment
            self.req_id += 1
            self.new_req = True

        for completed_req_id in completed_req_ids:
            # Record request delivery
            self.record_req_delivery(completed_req_id)  # Record Delivery moment            
            self.request_tardiness_costs.append(self._get_request_tardiness_cost(request=self.info[f"request_{completed_req_id}"]))
            self.assignee_agv_travel_costs.append(self._get_assignee_agv_travel_cost(request=self.info[f"request_{completed_req_id}"]))
            # Record the request stats in the master table
            self.record_req_stats(completed_req_id)
            del self.info[f"request_{completed_req_id}"]

    def create_request(self):
        """
        Creates a single request

        Returns
        -------
        [Tuple]
            [Origin and Dest Coordinates]
        """
        for parent in self.parents:
            if parent.is_temporal and not parent.is_active(
                self.info["day"], self.info["time"]
            ):
                continue
            if np.random.rand() < parent.arrival_rate:
                origin, dest = parent.get_random_source_dest()
                # sample a request cost
                request_cost = np.random.choice(self.request_costs)
                # sample a capability requirement
                capability_requirements = np.random.choice(self.capability_requirements)
                # Arrival time / earliest pickup time
                ept = self.now()
                # set latest delivery time
                ldt = self.now() + max(0, (self.max_dist/self.min_agv_speed) * random.uniform(0.1, 1.0) * self.inflation_factor)

                return origin, dest, ept, ldt, request_cost, capability_requirements

        return None, None, None, None, None, None

    def create_request_from_layout(self):
        """
        Creates a single request

        Returns
        -------
        [Tuple]
            [Origin and Dest Coordinates]
        """
        for parent in self.parents:
            if parent.is_temporal and not parent.is_active(
                self.info["day"], self.info["time"]
            ):
                continue
            if np.random.rand() < parent.arrival_rate:
                origin = parent.get_random_node()

                dest_parent = np.random.choice(self.parents)
                dest = dest_parent.get_random_node()

                while origin == dest:
                    dest_parent = np.random.choice(self.parents)
                    dest = dest_parent.get_random_node()

                # sample a request cost
                request_cost = np.random.choice(self.request_costs)
                # sample a capability requirement
                capability_requirements = np.random.choice(self.capability_requirements)
                # Arrival time / earliest pickup time
                ept = self.now()
                # set latest delivery time
                ldt = self.now() +  max(0, (self.max_dist/self.min_agv_speed) * random.uniform(0.1, 1.0) * self.inflation_factor)

                return origin, dest, ept, ldt, request_cost, capability_requirements

        return None, None, None, None, None, None

    def get_reposition_actions(self):	
        a_v = []	
        for i in range(self.n_AGVs):	
            v = self.info[f"V{i+1}"]	
            if v.is_eligible_for_reposition(env=self):
                if v.job_queue.get_job(0) == None or v.job_queue.get_job(0).type in [0, 1]:	
                    x, y = v.x, v.y	
                    tz = self.taxi_zones[(x, y)]	
                    # random_tz = np.random.randint(low=1, high=self.env.n_taxi_zones+1)	
                    a_v.append(tz)	
                    	
                else:	
                    a_v.append(0)	
            else:	
                a_v.append(0)	
        return a_v


    def step(self, action):
        """
        Executes an action in the simulation and increments time.

        Parameters
        ----------
        action : Action()
            an object of the Action class

        Returns
        -------
        (next_state, reward)
        """
 
        action_len = len(action)

        assert len(action)>= 1 and len(action) <= self.n_AGVs+1, "Length of action space should atleast be 1 and atmost equal to all agvs + 1, the AGV to which request is assigned, 0 otherwise"

        if action_len > 1: # marl action space
            a_r, a_v = action[0], action[1:]
        elif action_len == 1: # sarl action space
            a_r = action[0]
            a_v = self.get_reposition_actions()

        self.reward = 0.0
        self.request_tardiness_costs = []
        self.assignee_agv_travel_costs = []
        exp_wait_time = None
        exp_serve_time = None
        exp_request_tardiness_cost = 0.0
        exp_assignee_agv_travel_cost = 0.0
        inf_assignment = False
        req_rejected = False
        latest_request = None
        assignee_agv = None
        # a_r, a_v = self.get_user_action()

        # setting relocate jobs
        for i, a in enumerate(a_v):
            vehicle = self.info[f"V{i + 1}"]

            vehicle_loc = (vehicle.x, vehicle.y)

            # Vehicle is not allowed to idle at machines
            if a == 0 and vehicle_loc not in self.stations and vehicle.get_current_job() is None:
                # print('bad reposition')
                self.debug(f"Illegal reposition action on {vehicle}.")
                self.stats.agg_results["inf_reposition_count"] += 1
                self.reward += self.get_infeasible_reposition_reward(agv=vehicle)
                # assign to nearest CS
                
                a = self.taxi_zones[vehicle_loc]
                # print(f'AGV:{vehicle} was instructed to idle at machine at day: {self.now_day()}, time: {self.now_time()}, assigned TZ:{a}')
                done = True
                if self.terminate_on_infeasible_action:
                    # New_state, reward, done = True
                    return self.generate_state_dict(False), self.reward, done
                                
            if a==0:
                continue

            job_idx = vehicle.job_queue.get_preemptable_job_index()

            # if job queue is full
            if job_idx == 5:
                continue

            # otherwise, check if the agv is eligible for repositioning
            if not vehicle.is_eligible_for_reposition(env=self):
                self.debug(f"Illegal reposition action on {vehicle}.")
                # @Stat Increment infeasible action count
                self.stats.agg_results["inf_reposition_count"] += 1
                self.reward += self.get_infeasible_reposition_reward(agv=vehicle)
                done = True

                if self.terminate_on_infeasible_action:
                    # New_state, reward, done = True
                    return self.generate_state_dict(False), self.reward, done

            else:
                tz = a
                station = self._get_closest_station_tz(vehicle_loc, tz)
                
                vehicle.job_queue.set_job(
                    self, None, job_idx, 2, (vehicle.x, vehicle.y), station
                )

        # checking if agent was invoked by a new request state
        if self.invoked_by_new_req:
            latest_request = self.info[f"request_{self.req_id - 1}"]
            self.invoked_by_new_req = False
            # a_r = 0 means denial of request
            if a_r == 0:
                # print(f'Denying request {latest_request}')
                # @Stat Increment denied request count and type
                self.stats.record_rejected_request_stats(request=latest_request)
                self.reward += self.get_request_rejection_reward(request=latest_request)
                req_rejected = True
                del self.info[f"request_{self.req_id - 1}"]

            if a_r != 0:
                assignee_agv = self.info[f"V{a_r}"]

                # returning highly negative reward for choosing ineligible vehicle
                if not assignee_agv.is_eligible_for_assignment(request=latest_request):
                    self.debug(f"Illegal action on {assignee_agv}.")
                    self.stats.agg_results["inf_assignment_count"] += 1
                    inf_assignment = True
                    # @Stat Increment infeasible action count
                    self.stats.record_rejected_request_stats(request=latest_request)
                    
                    del self.info[f"request_{self.req_id - 1}"]

                    self.reward += self.get_infeasible_assignment_reward(request=latest_request)
                    done = True

                    if self.terminate_on_infeasible_action:
                        # New_state, reward, done = True
                        return self.generate_state_dict(False), self.reward, done

                else:
                    # Record assigned agv id
                    latest_request.assigned_agv_id = assignee_agv.id
                    # getting smallest preemtable job index
                    job_idx = assignee_agv.job_queue.get_preemptable_job_index()

                    # setting new request assignment job (preprocess)
                    assignee_agv_current_job = assignee_agv.get_current_job()

                    # If the current AGV is serving another request
                    if (
                        assignee_agv_current_job is not None
                        and assignee_agv_current_job.type == 4
                    ):
                        preprocess_job_src = assignee_agv_current_job.dest
                    else:
                        preprocess_job_src = (assignee_agv.x, assignee_agv.y)

                    assert (assignee_agv.charge >= assignee_agv.critical_charge_level), "AGV should atleast have a charge greater than its critical charge level at the time of request assignment"

                    assignee_agv.job_queue.set_job(
                        self,
                        latest_request.id,
                        job_idx,
                        3,
                        preprocess_job_src,
                        latest_request.origin,
                    )

                    # setting new request assignment job (serve)
                    assignee_agv.job_queue.set_job(
                        self,
                        latest_request.id,
                        job_idx + 1,
                        4,
                        latest_request.origin,
                        latest_request.dest,
                    )

                    # CALCULATE IMMEDIATE REQUEST AND AGV ASSIGNMENT STATS
                    self._set_request_est_delivery_time(request=latest_request, agv=assignee_agv)
                    exp_wait_time, exp_serve_time = self._get_exp_wait_serve_time(request=latest_request, agv=assignee_agv)
                    exp_request_tardiness_cost = self._get_request_exp_tardiness_cost(request=latest_request)
                    exp_assignee_agv_travel_cost = self._get_assignee_agv_exp_travel_cost(agv=assignee_agv, request=latest_request)

        # avg_incr = []
        # incrementing time till no new request or job completion
        while self.complete_req == False and self.new_req == False:
            # st = time.time()
            self.increment()
            # avg_incr.append(time.time() - st)
        # print("Average time for increment function: ", sum(avg_incr)/len(avg_incr))

        if self.complete_req:
            self.debug("Request(s) Completed")
            next_state_dict = self.generate_state_dict(False)
            self.complete_req = False

        if self.new_req:
            self.debug(f"New Request {self.info[f'request_{self.req_id - 1}']}")
            next_state_dict = self.generate_state_dict(True)
            self.new_req = False
            self.invoked_by_new_req = True

        done = False
        if self.agg_days >= self.horizon:
            done = True

        info = {}

        # CALCULATE FLEET TRAVEL STATS
        fleet_travel_costs = self._get_fleet_travel_costs()

        # Calculate total reward from doing a request assignment
        if not req_rejected and not inf_assignment:
            reward = self.get_reward(exp_request_tardiness_cost=exp_request_tardiness_cost, \
                exp_assignee_agv_travel_cost=exp_assignee_agv_travel_cost, \
                    exp_wait_time = exp_wait_time, exp_serve_time = exp_serve_time, \
                    request_tardiness_costs = self.request_tardiness_costs, \
                        assignee_agv_travel_costs = self.assignee_agv_travel_costs, \
                    fleet_travel_costs=fleet_travel_costs, request = latest_request, assigned_agv = assignee_agv)

            self.reward += reward

        return next_state_dict, self.reward, done, info

    def _set_request_est_delivery_time(self, *args, **kwargs):
        """
        Sets the estimated delivery time for the request.
        """

        request:Request = kwargs["request"]
        assignee_agv:AGV = kwargs["agv"]
        
        exp_wait_time, exp_serve_time = assignee_agv.get_exp_wait_and_serve_time(env=self, request=request)
        request.est_delivery_time = request.get_arrival_time() + exp_wait_time + exp_serve_time
    
    def _get_exp_wait_serve_time(self, *args, **kwargs):
        """
        Returns the expected wait and serve time for the request.
        """

        request:Request = kwargs["request"]
        assignee_agv:AGV = kwargs["agv"]
        
        exp_wait_time, exp_serve_time = assignee_agv.get_exp_wait_and_serve_time(env=self, request=request)
        return exp_wait_time, exp_serve_time

    def get_reward(self,*args, **kwargs):
        raise NotImplementedError("Must override get_reward")

    def get_infeasible_reposition_reward(self, *args, **kwargs):
        raise NotImplementedError("Must override get_infeasible_reposition_reward")

    def get_request_rejection_reward(self, *args, **kwargs):
        raise NotImplementedError("Must override get_request_rejection_reward")

    def get_infeasible_assignment_reward(self, *args, **kwargs):
        raise NotImplementedError("Must override get_infeasible_assignment_reward")
        

    def generate_state_dict(self, new_req_trigger):
        state_time = {
            'time_in_sec': self.info["time"],
            'day_number': self.info["day"]
            }

        request = None

        if new_req_trigger:
            new_req_id = self.req_id - 1
            request = self.info[f"request_{new_req_id}"]
            req_path = self.maze.solve(request.origin, request.dest)[0]
            req_dist = self.get_distance(req_path)

            state_request = {
                "new_req": int(new_req_trigger),
                "request_id": new_req_id,
                "request_origin_coordinates": request.origin,
                "request_dest_coordinates": request.dest,
                "distance_origin_dest": req_dist,
                "ept": request.ept,
                "ldt": request.ldt,
                "capability_requirements": request.capability_requirements,
                "request_cost": request.request_cost
                }

        else:

            state_request = {
                "new_req": int(new_req_trigger),
                "request_id": -1,
                "request_origin_coordinates": (-1, -1),
                "request_dest_coordinates": (-1, -1),
                "distance_origin_dest": -1,
                "ept": -1,
                "ldt": -1,
                "capability_requirements": -1,
                "request_cost": -1
                }


        state_fleet = {
                "num_agvs": self.n_AGVs,

        }
        for i in range(1, self.n_AGVs + 1):
            vehicle = self.info[f"V{i}"]
            vehicle.set_eta_and_eca(env=self)
            expected_location_at_availability = (vehicle.x, vehicle.y)

            if request != None:
                path = self.maze.solve(expected_location_at_availability, request.origin)[0]
                dist = self.get_distance(path)
                distance_from_active_request_dest_to_request_origin = dist

                if vehicle.get_current_job() is not None and vehicle.get_current_job().type==4: # serve job
                    expected_location_at_availability = tuple(vehicle.get_current_job().dest)
                    path = self.maze.solve(expected_location_at_availability, request.origin)[0]
                    distance_from_active_request_dest_to_request_origin = self.get_distance(path)

           


            state_fleet[f"agv{i}"] = {
                "velocity": vehicle.velocity,
                "charge": vehicle.charge,
                "location_coordinates": (vehicle.x, vehicle.y),
                "is_eligible_assignment": vehicle.is_eligible_for_assignment(request=request, env=self, check_eca=True) if request != None else -1,
                "is_eligible_reposition": vehicle.is_eligible_for_reposition(env=self),
                "expected_time_of_availability_sec": vehicle.eta + self.info["time"],
                "expected_charge_at_availability": vehicle.eca,
                "expected_location_at_availability": expected_location_at_availability,
                "capabilities": vehicle.capabilities,
                "travel_cost": vehicle.travel_cost,
                "distance_to_request_origin": dist if request !=None else -1,
                "distance_from_active_request_dest_to_request_origin": distance_from_active_request_dest_to_request_origin if request !=None else -1,
                "distance_to_center": math.sqrt((vehicle.x-self.length/(self.d_g*2))**2 + (vehicle.y-self.width/(self.d_g*2))**2)
            }

        return (state_time, state_request, state_fleet)


    def _get_request_exp_tardiness_cost(self, *args, **kwargs):
        """returns the expected tardiness cost of request
        """
        request:Request = kwargs["request"]
        return request.request_cost * max(0, (request.est_delivery_time - request.ldt))

    def _get_request_tardiness_cost(self, *args, **kwargs):
        """returns the tardiness cost of request
        """
        request:Request = kwargs["request"]
        return request.request_cost * max(0, (request.delivery_time - request.ldt))

    def _get_assignee_agv_travel_cost(self, *args, **kwargs):
        """returns the travel cost of assignee agv
        """
        request:Request = kwargs["request"]
        agv = self.info[f"V{request.assigned_agv_id}"]
        return agv.travel_cost * (request.delivery_time - request.arrival_time)

    def _get_assignee_agv_exp_travel_cost(self, *args, **kwargs):
        """returns the expected travel cost of assignee agv"""
        agv:AGV = kwargs["agv"]
        request:Request = kwargs["request"]

        return agv.travel_cost * (request.est_delivery_time - request.arrival_time)
        


    def _get_fleet_travel_costs(self, *args, **kwargs):
        """returns the total fleet travel costs
        """
        fleet_travel_costs = 0.0
        for i in range(1, self.n_AGVs + 1):
            vehicle:AGV = self.info[f"V{i}"]
            vehicle_travel_cost = vehicle.travel_cost * vehicle._get_travel_time_since_last_step()
            fleet_travel_costs += vehicle_travel_cost
            vehicle._reset_travel_time_since_last_step()
        
        return fleet_travel_costs



    def get_distance(self, directions):
            dist = 0
            for direction in directions:
                if direction in [1, 3, 5, 7]:
                    scaled_dist = self.d_dist
                elif direction in [0, 2, 4, 6]:
                    scaled_dist = self.s_dist
                dist += scaled_dist
            return dist

    def _get_euclidean_distance(self, x1, y1, x2, y2):
        return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

    def _get_closest_station_tz(self, loc, tz):

        stations_in_tz = self.get_stations_tz(tz)
        
        if len(stations_in_tz) == 1:
            return stations_in_tz[0] # returns the closest station in the tz

        min_dist = float('inf')
        closest_station = None
        for station in stations_in_tz:
            dist = self._get_euclidean_distance(loc[0], loc[1], station[0], station[1])
            if dist < min_dist:
                min_dist = dist
                closest_station = station
        return closest_station


    def _get_taxi_zone_from_loc(self, loc):
        return self.taxi_zones[loc]

    def _get_one_hot_encoding(self, idx_encoding=None, len_encoding=None):
        """Create a one-hot vector based on index and length of encoding

        Parameters
        ----------
        idx_encoding : [int]
            [the position at which to create the encoding]
        len_encoding : [int]
            [size of vector]

        Returns
        -------
        [list]
            [one hot encoded vector]
        """
        one_hot_encoding = [0] * len_encoding
        if idx_encoding is not None:
            one_hot_encoding[idx_encoding] = 1
        return one_hot_encoding

    def _normalize_time(self, time):
        """Normalizes time ( in second ) w.r.t. 1 day

        Parameters
        ----------
        time : [int]
            [time in seconds]

        Returns
        -------
        [float]
            [normalized time (time in sec / (24* 60 * 60)]
        """
        return time / (60 * 60 * 24)

   
    def render(self):
        """
        Renders the simulation in a user-friendly output. Show a request with a unique color and
        display the assigned AGV with the same color. This will help in tracking why AGVs are moving to
        certain nodes

        Parameters
        ----------
        None

        Returns
        -------
        None
        """

        if self.figure is None:
            self.figure, self.ax = plt.subplots()
            plt.rcParams["figure.figsize"] = (20, 40)
            plt.style.use("seaborn-white")
            # plt.ion()
            box = self.ax.get_position()
            self.ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

        ax = self.ax
        ax.clear()
        vehicle_coors_x = []
        vehicle_coors_y = []
        vehicle_color = []
        station_coors_x = []
        station_coors_y = []
        request_coors_src_x = []
        request_coors_src_y = []
        request_coors_dest_x = []
        request_coors_dest_y = []
        cs = 1

        for element_key in self.info:
            element = self.info[element_key]
            try:
                if element.obj_type == "agv":
                    vehicle_coors_x.append(element.x)
                    vehicle_coors_y.append(element.y)

                    if element.charge <= element.critical_charge_level:
                        vehicle_color.append("red")
                    elif element.charge <= 99:
                        vehicle_color.append("orange")
                    else:
                        vehicle_color.append("green")
                    # Annotation
                    # ax.annotate(f"{element.id}-{element.charge:.0f}%", xy=(element.x, element.y))
                if element.obj_type == "station":
                    station_coors_x.append(element.x)
                    station_coors_y.append(element.y)
                    # For Annotation
                    # ax.annotate(cs, xy=(element.x, element.y))
                    cs += 1
                if element.obj_type == "request":
                    request_coors_src_x.append(element.origin[0])
                    request_coors_src_y.append(element.origin[1])
                    request_coors_dest_x.append(element.dest[0])
                    request_coors_dest_y.append(element.dest[1])

            except AttributeError:
                if element_key == "day":
                    day = element
                if element_key == "time":
                    cur_time = element
                pass
        # fig, ax = plt.subplots()
        ax.set_ylim(0, self.y_range)
        ax.set_xlim(0, self.x_range)

        # Parents
        parent_colors = ["red", "blue", "brown", "yellow", "purple", "pink"]
        parent_indexer = 0
        for p, parent in enumerate(self.parents):
            ax.add_patch(
                Rectangle(
                    (parent.x, parent.y),
                    parent.length,
                    parent.width,
                    angle=0.0,
                    alpha=0.3,
                    label=f"Parent {p}",
                    color=parent_colors[parent_indexer],
                    fill=False,
                    linewidth=3,
                )
            )
            parent_indexer += 1

        # Taxi-Zones
        for i, division in enumerate(self.divisions):
            ax.add_patch(
                Rectangle(
                    (division[0][0], division[1][0]),
                    division[0][1] - division[0][0],
                    division[1][1] - division[1][0],
                    angle=0.0,
                    alpha=0.05,
                    label=f"TZ {i+1}",
                    color=self.temp["tz_colors"][i],
                )
            )

            # ax.annotate(
            #     f"TZ {i+1} \n CS:{self.closest_stations[i+1]}",
            #     xy=self.temp["tz_centers"][i],
            #     alpha=0.3,
            # )

        # Blocked
        ax.scatter(
            self.temp["blocked_x"],
            self.temp["blocked_y"],
            s=50,
            marker="s",
            color="red",
            label="Blocked Region",
        )
        # Stations
        ax.scatter(
            station_coors_x,
            station_coors_y,
            s=125,
            marker="H",
            label="Charging Stations",
        )
        # Children
        ax.scatter(
            self.temp["children_x"],
            self.temp["children_y"],
            s=50,
            color="#1b262c",
            marker="s",
        )
        # Request
        if request_coors_src_x:
            # ax.scatter(request_coors_src_x, request_coors_src_y, s=200, marker='*', color='orange', label='Active Requests')
            ax.scatter(
                request_coors_dest_x,
                request_coors_dest_y,
                s=25,
                marker="*",
                color="#00b7c2",
                label="Active Requests",
            )
            # print(request_coors_x, request_coors_y)
        try:
            latest_request = self.info["request_%d" % (self.req_id - 1)]
            ax.scatter(
                latest_request.origin[0],
                latest_request.origin[1],
                s=25,
                marker="*",
                color="#fdcb9e",
                label="Source Latest Request",
            )
            ax.scatter(
                latest_request.dest[0],
                latest_request.dest[1],
                s=25,
                marker="*",
                color="#fbd46d",
                label="Dest Latest Request",
            )

        except:
            pass
        # AGVs
        ax.scatter(
            vehicle_coors_x,
            vehicle_coors_y,
            s=25,
            marker="s",
            label="AGVs",
            color=vehicle_color,
        )

        # ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        ax.invert_yaxis()
        ax.set_xticks(ticks=self.temp["x_ticks"])
        ax.set_yticks(ticks=self.temp["y_ticks"])
        ax.grid(True)
        ax.set_title(f"Day:{day}, Time:{cur_time}")
        plt.pause(self.RENDER_PAUSE)
        plt.ion() # THIS ENABLES THE FIGURE TO UPDATE WITHOUT BLOCKING THE MAIN SCRIPT
        

    def plot_heat_map(self, data, ax=None):
        pass

    
    def get_user_action(self):
        a_r = int(
            input("Enter vehicle ID to be assigned to new request.\nEnter 0 to deny: ")
        )
        a_v = []
        for k in range(self.n_AGVs):
            temp = int(
                input(
                    "Enter station ID to assign vehicle %d to reposition to: " % (k + 1)
                )
            )
            a_v.append(temp)
        return a_r, a_v

    def dump_path_dict(self):
        self.maze.dump_path_dict()
        # print("Path dictionary dumped successfully.")

    def generate_paths_dict(self):
        print("Initiating the generation of unique paths.")
        print("Dumping path data at", self.maze.path_dict_filepath)

        src_dest_set = set()

        # # All department paths
        for parent in self.parents:
            for src_child in parent.loc_children:
                for dest_child in parent.loc_children:
                    if src_child != dest_child:
                        src_dest_set.add((src_child, dest_child))

        # All inter department paths
        for src_parent in self.parents:
            for dest_parent in self.parents:
                for src_child in src_parent.loc_children:
                    for dest_child in dest_parent.loc_children:
                        if src_child != dest_child:
                            src_dest_set.add((src_child, dest_child))


        # All station-station paths
        for src_station in self.stations:
            for dest_station in self.stations:
                if src_station != dest_station:
                    src_dest_set.add((src_station, dest_station))

        # All department-station
        for parent in self.parents:
            for src_child in parent.loc_children:
                for dest_station in self.stations:
                    if src_child != dest_station:
                        src_dest_set.add((src_child, dest_station))

        # All station - department
        for src_station in self.stations:
            for parent in self.parents:
                for dest_child in parent.loc_children:
                    if dest_child != src_station:
                        src_dest_set.add((src_station, dest_child))

        print(f"Number of unique source destination pairs:{len(src_dest_set)}")

        for i, src_dest_pair in enumerate(src_dest_set):
            origin, dest = src_dest_pair
            self.maze.solve(origin, dest)
            if i % 100 == 0:
                print(f"{i} combinations dumped")
                self.dump_path_dict()
        self.dump_path_dict()
        print("All possible combinations have been solved and dumped.")

    def debug(self, s):
        if self.is_debug_enabled:
            print(s)

    def now(self):
        """
        Return current day+time in Seconds

        Returns
        -------
        Float
            Time in seconds
        """
        return self.info["day"] * 24 * 60 * 60 + self.info["time"]

    def now_time(self):
        """
        Return current time in Seconds

        Returns
        -------
        Float
            Time in seconds
        """
        return self.info["time"]

    def now_day(self):
        """
        Return current day in integer

        Returns
        -------
        Float
            Day in integer
        """
        return self.info["day"]

    def record_req_arr(self, req_id):
        
        self.info[f"request_{req_id}"].arrival_day = self.now_day()
        self.info[f"request_{req_id}"].arrival_time = self.now()

    def record_req_pickup(self, req_id):
        request = self.info[f"request_{req_id}"]
        request.pickup_day = self.now_day()

        if request.pickup_day != request.arrival_day:
            request.pickup_time = (request.arrival_day + 1) * 24 * 60 * 60 + self.info["time"]

        else:
            self.info[f"request_{req_id}"].pickup_time = self.now()

    def record_req_delivery(self, req_id):

        request = self.info[f"request_{req_id}"]
        request.delivery_day = self.now_day()

        if request.delivery_day != request.pickup_day:
           
            request.delivery_time = (request.pickup_day + 1) * 24 * 60 * 60 + self.info["time"]
            self.debug('WARNING! Delivery day is not the same day as pickup day')
            self.debug(f'Adjusted pickup time: {request.pickup_time}. Adjusted delivery time: {request.delivery_time}')
            
        if request.delivery_day != request.arrival_day:
            request.delivery_time = (request.arrival_day + 1) * 24 * 60 * 60 + self.info["time"]

        else:
            request.delivery_time = self.now()



    def record_req_stats(self, completed_req_id):
        # Store stats of this completed request
        self.stats.record_request_stats(self.info["request_%d" % (completed_req_id)])

    def record_agv_stats(self):
        for element_key in self.info:
            element = self.info[element_key]
            try:
                if element.obj_type == "agv":
                    self.stats.record_agv_stats(element)
            except AttributeError:
                pass

    def get_detailed_stat_run(self):
        # Collect AGV Stats
        self.record_agv_stats()
        # Save All Results
        self.stats.save_results()

    def get_agg_stat_run(self):

        # Collect AGV Stats, request stats are updated after every request
        self.record_agv_stats()

        return self.stats.get_agg_stats()

    def tests(self):
        """Some Tests"""
        assert self.policy_type is not None, "policy_type cannot be none"
