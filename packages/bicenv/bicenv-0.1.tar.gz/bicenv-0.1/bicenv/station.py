class Station:

    def __init__(self, x, y):
        self.obj_type = "station"
        self.x = x
        self.y = y

    def __repr__(self):
        return f'Station at {(self.x, self.y)}'