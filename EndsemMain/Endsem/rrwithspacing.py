import numpy as np
import matplotlib.pyplot as plt

class Rectangle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def contains(self, point):
        return (self.x <= point[0] <= self.x + self.width and
                self.y <= point[1] <= self.y + self.height)

class Node:
    def __init__(self, point, parent=None):
        self.point = np.array(point)
        self.parent = parent

class RRT:
    def __init__(self, start, goal, bounds, obstacles, max_iters=1000, step_size=10):
        self.start = Node(start)
        self.goal = Node(goal)
        self.bounds = bounds
        self.obstacles = obstacles
        self.max_iters = max_iters
        self.step_size = step_size
        self.nodes = [self.start]

    def rand_point(self):
        return [np.random.uniform(self.bounds[0], self.bounds[0] + self.bounds[2]),
                np.random.uniform(self.bounds[1], self.bounds[1] + self.bounds[3])]

    def nearest_node(self, point):
        distances = [np.linalg.norm(np.array(node.point) - np.array(point)) for node in self.nodes]
        return self.nodes[np.argmin(distances)]

    def new_point(self, nearest, target):
        direction = np.array(target) - np.array(nearest.point)
        magnitude = np.linalg.norm(direction)
        if magnitude <= self.step_size:
            return target
        else:
            return nearest.point + (direction / magnitude) * self.step_size

    def is_collision(self, point):
        for obstacle in self.obstacles:
            if obstacle.contains(point):
                return True
        return False

    def generate_path(self):
        for _ in range(self.max_iters):
            random_point = self.random_point()
            nearest_node = self.nearest_node(random_point)
            new_point = self.new_point(nearest_node, random_point)
            if not self.is_collision(new_point):
                new_node = Node(new_point, nearest_node)
                self.nodes.append(new_node)
                if np.linalg.norm(np.array(new_point) - np.array(self.goal.point)) < self.step_size:
                    self.goal.parent = new_node
                    return True
        return False

    def backtrack_path(self):
        path = []
        current = self.goal
        while current is not None:
            path.append(current.point)
            current = current.parent
        return path[::-1]

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

# Modified RRT implementation with obstacle spacing consideration
class RRTWithSpacing(RRT):
    def __init__(self, start, goal, bounds, obstacles, spacing, max_iters=1000, step_size=10):
        super().__init__(start, goal, bounds, obstacles, max_iters, step_size)
        self.spacing = spacing

    def rand_point(self):
        while True:
            x = np.random.uniform(self.bounds[0] + self.spacing, self.bounds[0] + self.bounds[2] - self.spacing)
            y = np.random.uniform(self.bounds[1] + self.spacing, self.bounds[1] + self.bounds[3] - self.spacing)
            if all(not obstacle.contains([x, y]) for obstacle in self.obstacles):
                return [x, y]

# Example usage
start = (50, 50)
goal = (450, 450)
bounds = (0, 0, 500, 500)  # x, y, width, height
obstacles = [Rectangle(100, 100, 50, 50), Rectangle(300, 200, 70, 30), Rectangle(200, 400, 80, 40)]

rrt_with_spacing = RRTWithSpacing(start, goal, bounds, obstacles, spacing=20)
if rrt_with_spacing.generate_path():
    print("Path found!")
    rrt_with_spacing.plot()
else:
    print("Path not found!")

