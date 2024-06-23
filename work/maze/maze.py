import re
from typing import List, Tuple

class MazeError(Exception):
    pass

class Maze:
    def __init__(self, filename: str):
        self.filename = filename
        self.maze_grid = []
        self.xdim = 0
        self.ydim = 0
        self.load_maze_from_file()

    def load_maze_from_file(self):
        try:
            with open(self.filename, 'r') as file:
                lines = file.readlines()
        except FileNotFoundError:
            raise FileNotFoundError(f"File '{self.filename}' not found.")

        # Strip whitespace and filter out blank lines
        lines = [line.strip() for line in lines if line.strip()]

        # Check if the input is valid
        if not all(line.isdigit() and all(char in '0123' for char in line) for line in lines):
            raise MazeError("Incorrect input.")

        self.ydim = len(lines)
        self.xdim = len(lines[0])

        # Check if the maze dimensions are valid
        if not (2 <= self.xdim <= 31 and 2 <= self.ydim <= 41):
            raise MazeError("Input dimensions are invalid.")

        # Check if all lines have the same length
        if any(len(line) != self.xdim for line in lines):
            raise MazeError("Incorrect input.")

        # Check the last digit on every line and the digits on the last line
        if any(line[-1] in '13' for line in lines):
            raise MazeError("Input does not represent a maze.")
        if any(char in '23' for char in lines[-1]):
            raise MazeError("Input does not represent a maze.")

        # Convert the input to a 2D grid
        self.maze_grid = [[int(char) for char in line] for line in lines]

    def analyse(self):
        gates = self.count_gates()
        walls = self.analyze_walls()
        inaccessible_points = self.count_inaccessible_points()
        accessible_areas = self.count_accessible_areas()
        cul_de_sacs = self.analyze_cul_de_sacs()
        entry_exit_paths = self.count_entry_exit_paths()

        print(self.format_output("gate", gates))
        print(self.format_output("wall", walls))
        print(self.format_output("inaccessible inner point", inaccessible_points))
        print(self.format_output("accessible area", accessible_areas))
        print(self.format_output("accessible cul-de-sac", cul_de_sacs))
        print(self.format_output("entry-exit path with no intersection not to cul-de-sacs", entry_exit_paths))

    def count_gates(self) -> int:
        gates = 0
        for x in range(self.xdim):
            if self.maze_grid[0][x] == 0:
                gates += 1
            if self.maze_grid[self.ydim - 1][x] == 0:
                gates += 1
        for y in range(self.ydim):
            if self.maze_grid[y][0] == 0:
                gates += 1
            if self.maze_grid[y][self.xdim - 1] == 0:
                gates += 1
        return gates // 2

    def analyze_walls(self) -> int:
        visited = [[False] * self.xdim for _ in range(self.ydim)]
        wall_sets = 0

        def dfs(x, y):
            if x < 0 or x >= self.xdim or y < 0 or y >= self.ydim or visited[y][x] or self.maze_grid[y][x] == 0:
                return
            visited[y][x] = True
            neighbors = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
            for nx, ny in neighbors:
                if 0 <= nx < self.xdim and 0 <= ny < self.ydim and self.maze_grid[ny][nx] in [1, 2, 3]:
                    dfs(nx, ny)

        for y in range(self.ydim):
            for x in range(self.xdim):
                if not visited[y][x] and self.maze_grid[y][x] in [1, 2, 3]:
                    wall_sets += 1
                    dfs(x, y)

        return wall_sets

    def count_inaccessible_points(self) -> int:
        visited = [[False] * self.xdim for _ in range(self.ydim)]
        inaccessible_points = 0

        def dfs(x, y):
            if x < 0 or x >= self.xdim or y < 0 or y >= self.ydim or visited[y][x] or self.maze_grid[y][x] == 0:
                return
            visited[y][x] = True
            neighbors = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
            for nx, ny in neighbors:
                if 0 <= nx < self.xdim and 0 <= ny < self.ydim and self.maze_grid[ny][nx] in [1, 2, 3]:
                    dfs(nx, ny)

        for x in range(self.xdim):
            dfs(x, 0)
            dfs(x, self.ydim - 1)
        for y in range(self.ydim):
            dfs(0, y)
            dfs(self.xdim - 1, y)

        for y in range(1, self.ydim - 1):
            for x in range(1, self.xdim - 1):
                if not visited[y][x]:
                    inaccessible_points += 1

        return inaccessible_points

    def count_accessible_areas(self) -> int:
        visited = [[False] * self.xdim for _ in range(self.ydim)]
        accessible_areas = 0

        def dfs(x, y):
            if x < 0 or x >= self.xdim or y < 0 or y >= self.ydim or visited[y][x] or self.maze_grid[y][x] == 0:
                return
            visited[y][x] = True
            neighbors = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
            for nx, ny in neighbors:
                if 0 <= nx < self.xdim and 0 <= ny < self.ydim and self.maze_grid[ny][nx] in [1, 2, 3]:
                    dfs(nx, ny)

        for x in range(self.xdim):
            if self.maze_grid[0][x] in [1, 2, 3]:
                accessible_areas += 1
                dfs(x, 0)
            if self.maze_grid[self.ydim - 1][x] in [1, 2, 3]:
                accessible_areas += 1
                dfs(x, self.ydim - 1)
        for y in range(self.ydim):
            if self.maze_grid[y][0] in [1, 2, 3]:
                accessible_areas += 1
                dfs(0, y)
            if self.maze_grid[y][self.xdim - 1] in [1, 2, 3]:
                accessible_areas += 1
                dfs(self.xdim - 1, y)

        return accessible_areas

    def analyze_cul_de_sacs(self) -> int:
        visited = [[False] * self.xdim for _ in range(self.ydim)]
        cul_de_sacs = []

        def dfs(x, y, gate_x, gate_y):
            if x < 0 or x >= self.xdim or y < 0 or y >= self.ydim or visited[y][x] or self.maze_grid[y][x] == 0:
                return []
        visited[y][x] = True
        current_cul_de_sac = [(x, y)]
        neighbors = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        for nx, ny in neighbors:
            if 0 <= nx < self.xdim and 0 <= ny < self.ydim and self.maze_grid[ny][nx] in [1, 2, 3]:
                neighbor_cul_de_sac = dfs(nx, ny, gate_x, gate_y)
                if neighbor_cul_de_sac is not None:
                    current_cul_de_sac += neighbor_cul_de_sac
                elif (nx, ny) != (gate_x, gate_y):
                    return None
        return current_cul_de_sac

    for x in range(self.xdim):
        if self.maze_grid[0][x] in [1, 2, 3]:
            cul_de_sac = dfs(x, 0, x, 0)
            if cul_de_sac:
                cul_de_sacs.append(cul_de_sac)
        if self.maze_grid[self.ydim - 1][x] in [1, 2, 3]:
            cul_de_sac = dfs(x, self.ydim - 1, x, self.ydim - 1)
            if cul_de_sac:
                cul_de_sacs.append(cul_de_sac)
    for y in range(self.ydim):
        if self.maze_grid[y][0] in [1, 2, 3]:
            cul_de_sac = dfs(0, y, 0, y)
            if cul_de_sac:
                cul_de_sacs.append(cul_de_sac)
        if self.maze_grid[y][self.xdim - 1] in [1, 2, 3]:
            cul_de_sac = dfs(self.xdim - 1, y, self.xdim - 1, y)
            if cul_de_sac:
                cul_de_sacs.append(cul_de_sac)

    cul_de_sacs_sets = []
    visited_cul_de_sacs = set()
    for cul_de_sac in cul_de_sacs:
        cul_de_sac_set = set(cul_de_sac)
        if cul_de_sac_set not in visited_cul_de_sacs:
            cul_de_sacs_sets.append(cul_de_sac)
            visited_cul_de_sacs.add(cul_de_sac_set)

            return len(cul_de_sacs_sets)

def count_entry_exit_paths(self) -> int:
    visited = [[False] * self.xdim for _ in range(self.ydim)]
    entry_exit_paths = []

    def dfs(x, y, gate_x, gate_y, path):
        if x < 0 or x >= self.xdim or y < 0 or y >= self.ydim or visited[y][x] or self.maze_grid[y][x] == 0:
            return
        visited[y][x] = True
        path.append((x, y))
        neighbors = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        next_neighbors = []
        for nx, ny in neighbors:
            if 0 <= nx < self.xdim and 0 <= ny < self.ydim and self.maze_grid[ny][nx] in [1, 2, 3]:
                next_neighbors.append((nx, ny))
        if len(next_neighbors) == 2:
            path_copy1 = path.copy()
            path_copy2 = path.copy()
            dfs(next_neighbors[0][0], next_neighbors[0][1], gate_x, gate_y, path_copy1)
            dfs(next_neighbors[1][0], next_neighbors[1][1], gate_x, gate_y, path_copy2)
        elif len(next_neighbors) == 1:
            dfs(next_neighbors[0][0], next_neighbors[0][1], gate_x, gate_y, path)
        else:
            if (x, y) != (gate_x, gate_y):
                entry_exit_paths.append(path)

    for x in range(self.xdim):
        if self.maze_grid[0][x] in [1, 2, 3]:
            dfs(x, 0, x, 0, [])
        if self.maze_grid[self.ydim - 1][x] in [1, 2, 3]:
            dfs(x, self.ydim - 1, x, self.ydim - 1, [])
    for y in range(self.ydim):
        if self.maze_grid[y][0] in [1, 2, 3]:
            dfs(0, y, 0, y, [])
        if self.maze_grid[y][self.xdim - 1] in [1, 2, 3]:
            dfs(self.xdim - 1, y, self.xdim - 1, y, [])

    return len(entry_exit_paths)

def format_output(self, item_name: str, count: int) -> str:
    if count == 0:
        return f"The maze has no {item_name}."
    elif count == 1:
        return f"The maze has a unique {item_name}."
    else:
        return f"The maze has {count} {item_name}s."

def display(self):
    tex_file = f"{self.filename[:-4]}.tex"
    with open(tex_file, "w") as file:
        file.write(r"\documentclass{article}" + "\n")
        file.write(r"\usepackage{geometry}" + "\n")
        file.write(r"\usepackage{tikz}" + "\n")
        file.write(r"\begin{document}" + "\n")
        file.write(r"\begin{tikzpicture}[x=0.5cm, y=-0.5cm]" + "\n")

        # Draw walls
        file.write("% Walls\n")
        self.draw_walls(file)
        file.write("\n")

        # Draw pillars
        file.write("% Pillars\n")
        self.draw_pillars(file)
        file.write("\n")

        # Draw cul-de-sacs
        file.write("% Cul-de-sacs\n")
        self.draw_cul_de_sacs(file)
        file.write("\n")

        # Draw entry-exit paths
        file.write("% Entry-exit paths\n")
        self.draw_entry_exit_paths(file)

        file.write(r"\end{tikzpicture}" + "\n")
        file.write(r"\end{document}" + "\n")

def draw_walls(self, file):
    for y in range(self.ydim):
        x = 0
        while x < self.xdim:
            if self.maze_grid[y][x] in [1, 3]:
                x_start = x
                while x < self.xdim and self.maze_grid[y][x] in [1, 3]:
                    x += 1
                x_end = x
                file.write(r"\draw[blue] (%d,%d) -- (%d,%d);" % (x_start, y, x_end, y))
                x = x_end
                for x in range(self.xdim):
                    y = 0
        while y < self.ydim:
            if self.maze_grid[y][x] in [2, 3]:
                y_start = y
                while y < self.ydim and self.maze_grid[y][x] in [2, 3]:
                    y += 1
                y_end = y
                file.write(r"\draw[blue] (%d,%d) -- (%d,%d);" % (x, y_start, x, y_end))
            y = y_end

def draw_pillars(self, file):
    for y in range(self.ydim):
        for x in range(self.xdim):
            if self.maze_grid[y][x] == 0:
                file.write(r"\fill[green] (%d,%d) circle (0.15);" % (x, y))

def draw_cul_de_sacs(self, file):
    visited = [[False] * self.xdim for _ in range(self.ydim)]
    cul_de_sacs = []

    def dfs(x, y, gate_x, gate_y):
        if x < 0 or x >= self.xdim or y < 0 or y >= self.ydim or visited[y][x] or self.maze_grid[y][x] == 0:
            return []
        visited[y][x] = True
        current_cul_de_sac = [(x, y)]
        neighbors = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        for nx, ny in neighbors:
            if 0 <= nx < self.xdim and 0 <= ny < self.ydim and self.maze_grid[ny][nx] in [1, 2, 3]:
                neighbor_cul_de_sac = dfs(nx, ny, gate_x, gate_y)
                if neighbor_cul_de_sac is not None:
                    current_cul_de_sac += neighbor_cul_de_sac
                elif (nx, ny) != (gate_x, gate_y):
                    return None
        return current_cul_de_sac

    for x in range(self.xdim):
        if self.maze_grid[0][x] in [1, 2, 3]:
            cul_de_sac = dfs(x, 0, x, 0)
            if cul_de_sac:
                cul_de_sacs.append(cul_de_sac)
        if self.maze_grid[self.ydim - 1][x] in [1, 2, 3]:
            cul_de_sac = dfs(x, self.ydim - 1, x, self.ydim - 1)
            if cul_de_sac:
                cul_de_sacs.append(cul_de_sac)
    for y in range(self.ydim):
        if self.maze_grid[y][0] in [1, 2, 3]:
            cul_de_sac = dfs(0, y, 0, y)
            if cul_de_sac:
                cul_de_sacs.append(cul_de_sac)
        if self.maze_grid[y][self.xdim - 1] in [1, 2, 3]:
            cul_de_sac = dfs(self.xdim - 1, y, self.xdim - 1, y)
            if cul_de_sac:
                cul_de_sacs.append(cul_de_sac)

    for cul_de_sac in cul_de_sacs:
        for x, y in cul_de_sac:
            file.write(r"\fill[red] (%d,%d) cross (0.1);" % (x, y))

def draw_entry_exit_paths(self, file):
    visited = [[False] * self.xdim for _ in range(self.ydim)]
    entry_exit_paths = []

    def dfs(x, y, gate_x, gate_y, path):
        if x < 0 or x >= self.xdim or y < 0 or y >= self.ydim or visited[y][x] or self.maze_grid[y][x] == 0:
            return
        visited[y][x] = True
        path.append((x, y))
        neighbors = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        next_neighbors = []
        for nx, ny in neighbors:
            if 0 <= nx < self.xdim and 0 <= ny < self.ydim and self.maze_grid[ny][nx] in [1, 2, 3]:
                next_neighbors.append((nx, ny))
        if len(next_neighbors) == 2:
            path_copy1 = path.copy()
            path_copy2 = path.copy()
            dfs(next_neighbors[0][0], next_neighbors[0][1], gate_x, gate_y, path_copy1)
            dfs(next_neighbors[1][0], next_neighbors[1][1], gate_x, gate_y, path_copy2)
        elif len(next_neighbors) == 1:
            dfs(next_neighbors[0][0], next_neighbors[0][1], gate_x, gate_y, path)
        else:
            if (x, y) != (gate_x, gate_y):
                entry_exit_paths.append(path)

    for x in range(self.xdim):
        if self.maze_grid[0][x] in [1, 2, 3]:
            dfs(x, 0, x, 0, [])
        if self.maze_grid[self.ydim - 1][x] in [1, 2, 3]:
            dfs(x, self.ydim - 1, x, self.ydim - 1, [])
    for y in range(self.ydim):
        if self.maze_grid[y][0] in [1, 2, 3]:
            dfs(0, y, 0, y, [])
        if self.maze_grid[y][self.xdim - 1] in [1, 2, 3]:
            dfs(self.xdim - 1, y, self.xdim - 1, y, [])

    for entry_exit_path in entry_exit_paths:
        x_start, y_start = entry_exit_path[0]
        x_end, y_end = entry_exit_path[-1]
        file.write(r"\draw[yellow, dashed] (%d,%d) -- (%d,%d);" % (x_start, y_start, x_start + 0.25, y_start + 0.25))
        file.write(r"\draw[yellow, dashed] (%d,%d) -- (%d,%d);" % (x_end, y_end, x_end + 0.25, y_end + 0.25))

        for i in range(1, len(entry_exit_path)):
            x1, y1 = entry_exit_path[i - 1]
            x2, y2 = entry_exit_path[i]
            if x1 == x2:
                file.write(r"\draw[yellow, dashed] (%d,%d) -- (%d,%d);" % (x1, y1, x2, y2))
            else:
                file.write(r"\draw[yellow, dashed] (%d,%d) -- (%d,%d);" % (x1, y1, x2, y2))
                if name == "main":
                    maze = Maze("maze_1.txt")
                    maze.analyse()
                    maze.display()
