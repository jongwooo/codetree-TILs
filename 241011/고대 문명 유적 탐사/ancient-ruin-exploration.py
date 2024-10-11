from collections import deque

EMPTY = 0


def in_range(x, y):
    return 0 <= x < 5 and 0 <= y < 5


def find_max_value_coordinate():
    candidates = []
    for i in range(3):
        for j in range(3):
            for d in range(4):
                rotate(i, j)
                if d == 3:
                    break
                value = calculate_values()
                candidates.append((-value, d, j, i))
    candidates.sort()
    return candidates[0]


def rotate(sx, sy):
    global grid
    temp = [[0] * 5 for _ in range(5)]
    for x in range(sx, sx + 3):
        for y in range(sy, sy + 3):
            ox = x - sx
            oy = y - sy
            rx = oy
            ry = 3 - ox - 1
            temp[rx + sx][ry + sy] = grid[x][y]
    for x in range(sx, sx + 3):
        for y in range(sy, sy + 3):
            grid[x][y] = temp[x][y]


def calculate_values():
    value = 0
    visited = [[0] * 5 for _ in range(5)]
    for x in range(5):
        for y in range(5):
            if not visited[x][y]:
                value += bfs(x, y, visited)
    return value


def bfs(x, y, visited):
    queue = deque([(x, y)])
    visited[x][y] = 1
    num = grid[x][y]
    cnt = 1
    while queue:
        x, y = queue.popleft()
        for dx, dy in dirs:
            nx = x + dx
            ny = y + dy
            if in_range(nx, ny) and not visited[nx][ny] and grid[nx][ny] == num:
                queue.append((nx, ny))
                visited[nx][ny] = 1
                cnt += 1
    if cnt < 3:
        return 0
    return cnt


def update_grid(d, x, y):
    global grid
    for _ in range(d + 1):
        rotate(x, y)


def remove_used_items():
    value = 0
    visited = [[0] * 5 for _ in range(5)]
    for x in range(5):
        for y in range(5):
            if not visited[x][y]:
                value += bfs2(x, y, visited)
    return value


def bfs2(x, y, visited):
    global grid
    queue = deque([(x, y)])
    same_num_pos = deque([(x, y)])
    visited[x][y] = 1
    num = grid[x][y]
    cnt = 1
    while queue:
        x, y = queue.popleft()
        for dx, dy in dirs:
            nx = x + dx
            ny = y + dy
            if in_range(nx, ny) and not visited[nx][ny] and grid[nx][ny] == num:
                queue.append((nx, ny))
                same_num_pos.append((nx, ny))
                visited[nx][ny] = 1
                cnt += 1
    if cnt < 3:
        return 0
    while same_num_pos:
        x, y = same_num_pos.popleft()
        grid[x][y] = EMPTY
    return cnt


def fill_next_items_to_empty_space():
    global grid
    for y in range(5):
        for x in range(4, -1, -1):
            if grid[x][y] == EMPTY:
                grid[x][y] = next_items.popleft()


dirs = ((-1, 0), (0, 1), (1, 0), (0, -1))
K, M = map(int, input().split())
grid = [list(map(int, input().split())) for _ in range(5)]
next_items = deque(list(map(int, input().split())))
for _ in range(K):
    value, d, y, x = find_max_value_coordinate()
    if not value:
        break
    update_grid(d, x, y)
    value = remove_used_items()
    total_values = 0
    while value > 0:
        total_values += value
        fill_next_items_to_empty_space()
        value = remove_used_items()
    print(total_values, end=' ')