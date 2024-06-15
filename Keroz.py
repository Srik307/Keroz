import tkinter as tk

class Node:
    def __init__(self, x, y, obstacle=False):
        self.x = x
        self.y = y
        self.obstacle = obstacle
        self.g_cost = 0  # Cost from start to current node
        self.h_cost = 0  # Heuristic cost (estimated cost to reach destination)
        self.f_cost = 0  # Total cost: f_cost = g_cost + h_cost
        self.parent = None

# Function to calculate the Manhattan distance heuristic
def calculate_heuristic(current_node, destination_node):
    return abs(current_node.x - destination_node.x) + abs(current_node.y - destination_node.y)

# A* Pathfinding function
def astar_pathfinding(start, destination, grid):
    open_set = [start]
    closed_set = []

    while open_set:
        current_node = open_set[0]
        current_index = 0

        # Find node with lowest f_cost in the open_set
        for index, node in enumerate(open_set):
            if node.f_cost < current_node.f_cost:
                current_node = node
                current_index = index

        open_set.pop(current_index)
        closed_set.append(current_node)

        if current_node == destination:
            path = []
            while current_node is not None:
                path.append((current_node.x, current_node.y))
                current_node = current_node.parent
            return path[::-1]  # Reversed path from start to destination

        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]:  # Adjacent positions
            node_position = (current_node.x + new_position[0], current_node.y + new_position[1])

            # Check if node is within bounds
            if node_position[0] > (len(grid) - 1) or node_position[0] < 0 or node_position[1] > (len(grid[0]) - 1) or node_position[1] < 0:
                continue

            # Check if the node is an obstacle
            if grid[node_position[0]][node_position[1]].obstacle:
                continue

            children.append(grid[node_position[0]][node_position[1]])

        for child in children:
            if child in closed_set:
                continue

            child.g_cost = current_node.g_cost + 1
            child.h_cost = calculate_heuristic(child, destination)
            child.f_cost = child.g_cost + child.h_cost
            child.parent = current_node

            if child not in open_set:
                open_set.append(child)

# Create a function to visualize the grid and obstacles using Tkinter
def draw_grid():
    for x in range(len(grid)):
        for y in range(len(grid[x])):
            color = 'white'
            if grid[x][y].obstacle:
                color = 'black'
            canvas.create_rectangle(x * 20, y * 20, (x + 1) * 20, (y + 1) * 20, fill=color)
    root.update()

# Function to handle user click events and place obstacles
def place_obstacle(event):
    x = event.x // 20
    y = event.y // 20
    if not grid[x][y].obstacle:
        grid[x][y].obstacle = True
        draw_grid()

# Function to move the ball along the path
def move_ball(a,b):
    start_node = Node(a,b)
    destination_node = grid[99][99]
    path = astar_pathfinding(start_node, destination_node, grid)
    ob=-1
    if path:
        for i in range(len(path)):
            x, y = path[i]
            if(grid[x][y].obstacle):
                print('here is an obstacle')
                ob=i
                break
            else:
                ob=-1
            canvas.create_oval(x * 20, y * 20, (x + 1) * 20, (y + 1) * 20, fill='blue')
            if i > 0:
                prev_x, prev_y = path[i - 1]
                canvas.create_oval(prev_x * 20, prev_y * 20, (prev_x + 1) * 20, (prev_y + 1) * 20, fill='white')
            root.update()
            root.after(500)  # Add a delay for visualization
        if(ob==-1):
         canvas.create_oval(0, 0, 20, 20, fill='green')  # Start node
         canvas.create_oval(1800, 1800, 2000, 2000, fill='green')  # Destination node
         root.update()
         return 1
        else:
          print("let do iteration again")
          return path[ob-1]


# Initialize the Tkinter window and canvas
root = tk.Tk()
root.title("Ball Pathfinding Game")
canvas = tk.Canvas(root, width=900, height=900)
canvas.pack()

# Create a grid of nodes
grid = [[Node(x, y) for y in range(100)] for x in range(100)]

# Bind mouse click to place obstacles
canvas.bind("<Button-1>", place_obstacle)

# Draw initial grid
draw_grid()

def move():
    r=[0,0]
    while(r!=1):
     r=move_ball(r[0],r[1])

# Button to trigger ball movement along the path
##move_ball_button = tk.Button(root, text="Move Ball", command=move)
#move_ball_button.pack()
move()

root.mainloop()
