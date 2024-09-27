from collections import deque


def rotate(level):
    global grid
    temp = [[0] * grid_size for _ in range(grid_size)]
    size = 2 ** level
    half_size = 2 ** (level - 1)
    for x in range(0, grid_size, size):
        for y in range(0, grid_size, size):
            if half_size == 1:
                for i in range(half_size + 1):
                    for j in range(half_size + 1):
                        temp[x + j][half_size - i + y] = grid[x + i][y + j]
            else:
                for i in range(0, size, half_size):
                    for j in range(0, size, half_size):
                        for k in range(half_size):
                            for m in range(half_size):
                                temp[x + j + k][half_size - i + y + m] = grid[x + i + k][y + j + m]
    grid = temp


def melt():
    melt_candidates = []
    for x in range(grid_size):
        for y in range(grid_size):
            cnt = 0
            for dx, dy in dirs:
                nx = x + dx
                ny = y + dy
                if 0 <= nx < grid_size and 0 <= ny < grid_size and grid[nx][ny] > 0:
                    cnt += 1
            if cnt < 3 and grid[x][y] != 0:
                melt_candidates.append((x, y))
    for x, y in melt_candidates:
        grid[x][y] -= 1


def bfs():
    global ice_sum, max_cluster_size
    visited = [[False] * grid_size for _ in range(grid_size)]
    for i in range(grid_size):
        for j in range(grid_size):
            cluster_size = 0
            if visited[i][j] or grid[i][j] == 0:
                continue
            queue = deque([(i, j)])
            visited[i][j] = True
            while queue:
                x, y = queue.popleft()
                ice_sum += grid[x][y]
                cluster_size += 1
                for dx, dy in dirs:
                    nx = x + dx
                    ny = y + dy
                    if 0 <= nx < grid_size and 0 <= ny < grid_size and not visited[nx][ny] and grid[nx][ny] != 0:
                        queue.append((nx, ny))
                        visited[nx][ny] = True
            max_cluster_size = max(max_cluster_size, cluster_size)


n, q = map(int, input().split())
grid_size = 2 ** n
grid = [list(map(int, input().split())) for _ in range(grid_size)]
levels = list(map(int, input().split()))
dirs = ((-1, 0), (1, 0), (0, 1), (0, -1))
for level in levels:
    if level > 0:
        rotate(level)
    melt()
ice_sum = 0
max_cluster_size = 0
bfs()
print(ice_sum)
print(max_cluster_size)