from collections import deque

# Breadth-First Search (BFS)
def bfs(grid, start, end):
    rows, cols = len(grid), len(grid[0])
    visited = set()
    queue = deque([(start, [start])])

    while queue:
        (r, c), path = queue.popleft()

        if (r, c) == end:
            return path

        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                if grid[nr][nc] != 1 and (nr, nc) not in visited:
                    visited.add((nr, nc))
                    queue.append(((nr, nc), path + [(nr, nc)]))

    return None


# Depth-First Search (DFS) - not used, but provided as an option for customization
def dfs(grid, start, end):
    rows, cols = len(grid), len(grid[0])
    visited = set()
    stack = [(start, [start])]

    while stack:
        (r, c), path = stack.pop()

        if (r, c) == end:
            return path

        if (r, c) not in visited:
            visited.add((r, c))
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != 1:
                    stack.append(((nr, nc), path + [(nr, nc)]))

    return None

# NOTE: Currently the game uses BFS by default. You can switch to DFS or add other algorithms
# by calling `dfs(grid, start, end)` instead of `bfs(...)` wherever pathfinding is needed.
