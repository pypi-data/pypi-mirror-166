import numpy as np

class Parent:

    def __init__(self, *args, **kwargs):
        self.parent_id = kwargs['parent_id']
        self.parent_type = kwargs['parent_type']
        self.x = kwargs['x']
        self.y = kwargs['y']
        self.width = kwargs['width']
        self.length = kwargs['length']
        self.arrival_rate = kwargs['arrival_rate']
        self.is_temporal = kwargs['is_temporal']
        self.active_days = kwargs['active_days']
        self.start_times = kwargs['start_times']
        self.durations = kwargs['durations']
        self.loc_children = list()
        self.num_children = None
        self.max_dist = (self.length ** 2 + self.width ** 2) ** (1 / 2)

    def get_max_dist(self):
        """
        Returns max dist in the layout
        """
        return self.max_dist

        

    def is_active(self, day, time):
        """
        Checks whether the parent is active in the given simulation time

        Parameters
        ----------
        day : Integer
            Day of the week
        time : Integer
            Time of the day

        Returns
        -------
        Boolean
            whether the hotspot is active
        """
        active_day = day in self.active_days
        if not active_day:
            return False
        
        for start_time, duration in zip(self.start_times,self.durations):
            active_time = time >= start_time and time <= start_time + duration
            if active_time:
                return True
        return False


    def get_random_source_dest(self):
        """Returns a random source and destination pair

        Returns
        -------
        [tuple of tuples]
            source and destination coordinate pairs
        """
        
        source = int(np.random.randint(self.num_children))
        dest = int(np.random.randint(self.num_children))
        src_loc = self.loc_children[source]
        dst_loc = self.loc_children[dest]

        while src_loc == dst_loc:
            source = int(np.random.randint(self.num_children))
            dest = int(np.random.randint(self.num_children))
            src_loc = self.loc_children[source]
            dst_loc = self.loc_children[dest]

        return src_loc, dst_loc

    def get_random_node(self):
        """Returns a random source and destination pair

        Returns
        -------
        [tuple of tuples]
            source and destination coordinate pairs
        """
        
        node = int(np.random.randint(self.num_children))
        
        node_loc = self.loc_children[node]

        return node_loc



        

        


        