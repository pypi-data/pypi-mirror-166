import numpy as np


class Request:

    def __init__(self, id, origin, dest, ept, ldt, request_cost, capability_requirements):
        self.id = id
        self.obj_type = "request"
        self.elapsed_time = 0
        self.origin = origin
        self.dest = dest
        self.ept = ept
        self.ldt = ldt
        self.completed = False
        self.request_cost = request_cost  # Cost can be based on priority
        self.capability_requirements = capability_requirements

        # Statistics
        self.arrival_day = None
        self.arrival_time = None
        self.pickup_day = None
        self.pickup_time = None
        self.delivery_day = None
        self.delivery_time = None
        self.est_pickup_time = None
        self.est_delivery_time = None
        self.assigned_agv_id = None

    def __repr__(self):
        return f'ID_{self.id}, Origin:{self.origin}, Destination:{self.dest}'

    def get_arrival_time(self):
        if self.arrival_time == None:
            raise RuntimeError(f"Request:{self} cannot have NONE arrival time.")
        return self.arrival_time