
class PDNode:

    def __init__(self, *args, **kwargs):
        """
        PD object
        """
        self.parent_id = kwargs['parent_id']            # the department id to which the machine belongs
        self.name = kwargs['name']                          # name of the machine
        self.x = kwargs['x']                                # x-coordinate in meters
        self.y = kwargs['y']                                # y-coordinate in meters
        self.arrival_pattern = kwargs['arrival_pattern']    # probably a matrix of size [day in a week, hours in a day]
        self.type = kwargs['pd_type']                       # Type of Node -> "machine" or "storage"

        

    
