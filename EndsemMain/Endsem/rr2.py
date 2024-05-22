#Importing essential libraries 
import numpy as np
import matplotlib.pyplot as plt
#Defining a class to initialize the environment as a rectangle , with a certain width and height
class Environment:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def contains(self, point):
        return (self.x <= point[0] <= self.x + self.width and
                self.y <= point[1] <= self.y + self.height)
#Defining a class to generate nodes
class Node:
    def __init__(self, point, parent=None):
        self.point = np.array(point)
        self.parent = parent
#Defining class for RRT parameters
class RRT:
    def __init__(self, start, goal, bounds, obstacles, max_iters=1000, step_size=10):
        self.start = Node(start)
        self.goal = Node(goal)
        self.bounds = bounds
        self.obstacles = obstacles
        self.max_iters = max_iters
        self.step_size = step_size
        self.nodes = [self.start]
#Generating Random points in vicinity of current node of tree
    def rand_point(self):
        return [np.random.uniform(self.bounds[0], self.bounds[0] + self.bounds[2]),
                np.random.uniform(self.bounds[1], self.bounds[1] + self.bounds[3])]
#Returning nearest distance node
    def nearest_node(self, point):
        distances = [np.linalg.norm(np.array(node.point) - np.array(point)) for node in self.nodes]
        return self.nodes[np.argmin(distances)]
#Creating new point at this nearest distance
    def new_point(self, nearest, target):
        direction = np.array(target) - np.array(nearest.point)
        magnitude = np.linalg.norm(direction)
        if magnitude <= self.step_size:
            return target
        else:
            return nearest.point + (direction / magnitude) * self.step_size
#Check if path lies outside obstacle
    def check_collision(self, point):
        for obstacle in self.obstacles:
            if obstacle.contains(point):
                return True
        return False
#Create a path connecting this node and point
    def create_path(self):
        for _ in range(self.max_iters):
            random_point = self.rand_point()
            nearest_node = self.nearest_node(random_point)
            new_point = self.new_point(nearest_node, random_point)
            if not self.check_collision(new_point):
                new_node = Node(new_point, nearest_node)
                self.nodes.append(new_node)
                if np.linalg.norm(np.array(new_point) - np.array(self.goal.point)) < self.step_size:
                    self.goal.parent = new_node
                    return True
        return False
#Backtrack the path from the goal node to the start node in the tree
    def backtrack_path(self):
        path = []
        current = self.goal
        while current is not None:
            path.append(current.point)
            current = current.parent
        return path[::-1]
#Plotting the entire layout
    def plot(self):
        plt.figure(figsize=(8, 8))
        plt.axis('equal')
        plt.plot(self.start.point[0], self.start.point[1], 'go', markersize=10)
        plt.plot(self.goal.point[0], self.goal.point[1], 'ro', markersize=10)
        for obstacle in self.obstacles:
            plt.gca().add_patch(plt.Rectangle((obstacle.x, obstacle.y), obstacle.width, obstacle.height, color='gray'))
        for node in self.nodes:
            if node.parent:
                plt.plot([node.point[0], node.parent.point[0]], [node.point[1], node.parent.point[1]], 'k-')
        path = self.backtrack_path()
        if path:
            plt.plot([point[0] for point in path], [point[1] for point in path], 'b-')
        plt.xlim(self.bounds[0], self.bounds[0] + self.bounds[2])
        plt.ylim(self.bounds[1], self.bounds[1] + self.bounds[3])
        plt.show()

# We Define start and goal points, which can be modified appropriately
start = (50, 50)
goal = (450, 450)
# x, y, width, height respectively , for all below parameters
bounds = (0, 0, 500, 500) 
#We define width and height of parameters 
obstacles = [Environment(110, 150, 50, 50), Environment(200, 250, 70, 30), Environment(400, 400, 80, 40)] #

rrt = RRT(start, goal, bounds, obstacles)
#This caters to whether the algorithm was able to obtain a path between the necessary positions 
if rrt.create_path():
    print("Successful Path Obtained")
    rrt.plot()
else:
    print("No Path Detected")
