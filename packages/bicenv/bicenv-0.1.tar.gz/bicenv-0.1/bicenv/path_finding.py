import math
import json
#from environment import Environment
import typing 
import pickle
from filelock import FileLock, Timeout
import os
from typing import Tuple, Any, List
# from queue import PriorityQueue

class Node():
    """
        Data Structure to represent

        Parameters
        ----------
        state : Tuple[int,int]
            x and y coordinates of the node
        parent : [type]
            Parent node
        action : int
            direction from parent
            0 N, 1 NE, 2 E, 3 SE, 4 S, 5 SW, 6 W, 7 NW
        md : float, optional
            Manhattan Distance, by default None
        """

    def __init__(self, state:Tuple[int,int], parent:'Node', action:int,md:float=None):
        self.state = state
        self.parent = parent
        self.action = action
        self.manhattan_dist = md

    def __repr__(self):
        return f'{self.state}'

class StackFrontier():
    """
    Queue that facilitates depth-first search
    """
    def __init__(self):
        self.frontier:List[Node] = []

    def add(self, node:Node):
        """
        Add node to queue

        Parameters
        ----------
        node : Node
            Node to add in the Queue
        """
        self.frontier.append(node)

    def contains_state(self, state:Tuple[int,int])->bool:
        """
        Checks whether state is already stored in frontier(Queue)

        Parameters
        ----------
        state : Tuple[int,int]
            

        Returns
        -------
        bool
            True, if the Queue contains the node
        """
        return any(node.state == state for node in self.frontier)

    def empty(self)->bool:
        """
        Checks if the Queue is empty

        Returns
        -------
        bool
            True, if queue is empty
        """
        return len(self.frontier) == 0

    def remove(self)->Node:
        """
        Removes the node from Queue

        Returns
        -------
        Node
            

        Raises
        ------
        Exception
            If Queue is empty
        """
        if self.empty():
            raise Exception('empty frontier')

        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node

class QueueFrontier(StackFrontier):
    """
    Breadth First Search Queue implementation

    Parameters
    ----------
    StackFrontier : Base Class
        
    """
    def remove(self):
        """
        Removes the node from Queue

        Returns
        -------
        Node
            

        Raises
        ------
        Exception
            If Queue is empty
        """
        if self.empty():
            raise Exception('empty frontier')
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node

class PriorityQueue(StackFrontier):
    """
    Best-First Search Queue implementation

    Parameters
    ----------
    StackFrontier : Base Class
        
    """
    def add(self, node:Node):
        """
        adds a new node based on its rank (lower manhattan distance is higher rank)

        Parameters
        ----------
        node : Node
            Node to add
        """
        self.frontier.append(node)
        self.frontier = sorted(self.frontier, key=lambda x:x.manhattan_dist)


    def remove(self)->Node:
        """
        Removes the node from Queue

        Returns
        -------
        Node
            

        Raises
        ------
        Exception
            If Queue is empty
        """
        if self.empty():
            raise Exception('empty frontier')
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node

class Maze():
    """
        Alternate representation of the environment to solve path planning

        Parameters
        ----------
        env : Environment
            
        config : Any
            JSON file with information about blocked grids 
        """

    def __init__(self, grid, config):
        self.grid = grid.copy()
        self.height = grid.shape[1]
        self.width = grid.shape[0]
        if type(config)=='str':
            with open(config, 'r') as f:
                config = json.load(f)
        with open(config["layout_config_file"], 'r') as f:
                config_layout = json.load(f)       
        self.blocked = config_layout['Blocked'] # DEBUG: Possibly wrong at the moment
        self.path_dict_filepath = config['path_dict_file']
        try:
            lock = FileLock(self.path_dict_filepath + ".lock", timeout=10)
            with lock:
                with open(self.path_dict_filepath, 'rb') as infile:
                    self.path_dict = pickle.load(infile)
            
        except (FileNotFoundError, PermissionError) as e:
            print("Paths dictionary pickle not found.")
            self.path_dict = {}
        self.mark_blocked()
        self.dir_key={0:'N', 1:'NE',2: 'E', 3: 'SE', 4: 'S', 5: 'SW', 6: 'W', 7: 'NW'}
        
        

    def render(self):
        """
        Renders the environment and solution
        """
        render_array = list([[' ' for x in range(self.width)] for y in range(self.height)])
        for blocked in self.blocked:
            x, y = blocked
            render_array[y][x] = "█"
        
        try:
            for coord in self.solution[1]:
                x, y = coord
                render_array[y][x] = '*'
            render_array[self.goal[1]][self.goal[0]] = 'D'
            render_array[self.start[1]][self.start[0]] = 'S'
            
            for row in render_array:
                print(row)
            
        except:
            for row in render_array:
                print(row)
            pass


    def mark_blocked(self):
        """
        Sets all the blocked elements in the grid
        """
        # blocked = self.env.blo
        #print(self.blocked)
        for blocked in self.blocked:
            print(blocked)
            x, y = blocked
            self.grid[x,y] = 1
        # print(self.grid)
        

    def get_manhattan_dist(self, state:Tuple[int,int])->int:
        """
        return the manhattan distance between state and goal
        Formula: absolute(state_x - dest_x) + absolute(dest_x - dest_y)

        Parameters
        ----------
        state : Tuple[int,int]
            

        Returns
        -------
        int
            Manhattan Distance
        """
        xs, ys = state
        xd, yd = self.goal
        return abs(xd-xs)+abs(yd-ys)

    def neighbors(self, state:Tuple[int,int]):
        """
        Return valid neighbors from state location, walls are represented by 1 in self.grid

        Parameters
        ----------
        state : Tuple[int,int]
            

        Returns
        -------
        [Any]
            Valid neghbors from state location
        """
        x, y = state
        # 0 N, 1 NE, 2 E, 3 SE, 4 S, 5 SW, 6 W, 7 NW
        candidates = [
            (0, self.get_manhattan_dist((x, y-1)), (x, y-1)),
            (1, self.get_manhattan_dist((x+1, y-1)), (x+1, y-1)),
            (2, self.get_manhattan_dist((x+1, y)), (x+1, y)),
            (3, self.get_manhattan_dist((x+1, y+1)), (x+1, y+1)),
            (4, self.get_manhattan_dist((x, y+1)), (x, y+1)),
            (5, self.get_manhattan_dist((x-1, y+1)), (x-1, y+1)),
            (6, self.get_manhattan_dist((x-1, y)), (x-1, y)),
            (7, self.get_manhattan_dist((x-1, y-1)), (x-1, y-1))
            ]

        result=[]
        for action, md, (new_x, new_y) in candidates:
            if 0<=new_y<self.height and 0<=new_x<self.width:
                if self.grid[new_x,new_y]!=1:
                    result.append((action, md, (new_x,new_y)))
        return result


    def solve(self, origin:Tuple[int,int], dest:Tuple[int,int])->Any:
        """
        Solves the grid

        Raises
        ------
        Exception
            No solution found if frontier is empty without goal state

        Returns
        --------
        [Any]
            Directions to go from source to destination, and the coordinates visited
            Example:
            directions, coord = maze.solve()
        """

        #Reset the grid and Mark Source and Destination
# ````````self.grid = np.where(self.grid==8 | self.grid==9, 0)
        
        #Mark source and destination
        if origin in self.path_dict:
            if dest in self.path_dict[origin]:
                return self.path_dict[origin][dest]
        else:
            self.path_dict[origin] = {}
        xs, ys = origin
        xd, yd = dest

        self.start = origin
        self.goal = dest

        # self.grid[yd,xd] = 9
        # self.grid[ys,xs] = 8
        self.grid[xd, yd] = 9
        self.grid[xs, ys] = 8


        #Solve
        self.num_explored = 0
        start = Node(state = origin, parent = None, action = None)

        frontier = PriorityQueue()
        # frontier = QueueFrontier()
        # frontier = StackFrontier()
        frontier.add(start)
        self.explored = set()

        while True:

            if frontier.empty():
                raise Exception('no solution')

            node = frontier.remove()
            self.num_explored += 1

            if node.state == dest:
                actions = []
                cells = []
                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent
                actions.reverse()
                cells.reverse()
                self.solution = (actions, cells)
                #reset the grid state
                # self.grid[yd,xd] = 0
                # self.grid[ys,xs] = 0
                self.grid[xd,yd] = 0
                self.grid[xs,ys] = 0
                #return solution
                self.path_dict[origin][dest] = self.solution
                return self.solution

            self.explored.add(node.state)

            for action, md, state in self.neighbors(node.state):
                if not frontier.contains_state(state) and state not in self.explored:
                    child = Node(state=state, parent = node, action =action, md=md)
                    frontier.add(child)
    
    def dump_path_dict(self):
        try:
            lock = FileLock(self.path_dict_filepath + ".lock", timeout=10)
            with lock:
                with open(self.path_dict_filepath, 'wb') as outfile:
                    pickle.dump(self.path_dict, outfile)
        except PermissionError:
            print('Permission error to write path pickles.')
            return 0
        # print("Path dictionary dumped successfully.")

    def print_solution(self):
        """
        Prints the solution in an interpretable fashion
        """
        for action in self.solution[0]:
            print(f'{action}:{self.dir_key[action]}, ', end="")



#if __name__ =='__main__':       
#    env = Environment('Configs/config_prototype.json')
#    maze = Maze(env.grid, config = 'Configs/config_prototype.json')
#    maze.render()
#    sol, coord = maze.solve( (3,6), (20,20))
#    print("--------------------------------Solved Grid------------------------------------------------")
#    maze.render()
#    print(f'Solution found in {maze.num_explored} steps')
#    print(sol)
#    maze.print_solution()