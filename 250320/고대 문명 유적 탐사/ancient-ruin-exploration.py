import heapq
from collections import deque

GRID_SIZE = 5
EXPLORATION_SIZE = 3
EMPTY = 0


def in_range(x, y):
    return 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE


def rotate_90(sx, sy):
    global grid
    temp = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
    for x in range(sx, sx + EXPLORATION_SIZE):
        for y in range(sy, sy + EXPLORATION_SIZE):
            ox = x - sx
            oy = y - sy
            rx = oy
            ry = EXPLORATION_SIZE - ox - 1
            temp[sx + rx][sy + ry] = grid[x][y]
    for x in range(sx, sx + EXPLORATION_SIZE):
        for y in range(sy, sy + EXPLORATION_SIZE):
            grid[x][y] = temp[x][y]


def find_max_value_coordinate():
    value_candidates = []
    for sx in range(EXPLORATION_SIZE):
        for sy in range(EXPLORATION_SIZE):
            for d in range(4):
                rotate_90(sx, sy)
                if d == 3:
                    break
                visited = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
                value = 0
                for x in range(GRID_SIZE):
                    for y in range(GRID_SIZE):
                        if not visited[x][y]:
                            value += bfs1(x, y, visited)
                heapq.heappush(value_candidates, (-value, d, sy, sx))
    return heapq.heappop(value_candidates)


def bfs1(x, y, visited):
    queue = deque([(x, y)])
    visited[x][y] = 1
    item_num = grid[x][y]
    value = 1
    while queue:
        x, y = queue.popleft()
        for dx, dy in dirs:
            nx = x + dx
            ny = y + dy
            if in_range(nx, ny) and not visited[nx][ny] and grid[nx][ny] == item_num:
                queue.append((nx, ny))
                visited[nx][ny] = 1
                value += 1
    if value < 3:
        value = 0
    return value


def update_grid(sx, sy, d):
    for _ in range(d + 1):
        rotate_90(sx, sy)


def remove_used_items_from_grid():
    visited = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
    value = 0
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            if not visited[x][y]:
                value += bfs2(x, y, visited)
    return value


def bfs2(x, y, visited):
    global grid
    queue = deque([(x, y)])
    visited[x][y] = 1
    item_num = grid[x][y]
    same_item_coordinates= deque([(x, y)])
    while queue:
        x, y = queue.popleft()
        for dx, dy in dirs:
            nx = x + dx
            ny = y + dy
            if in_range(nx, ny) and not visited[nx][ny] and grid[nx][ny] == item_num:
                queue.append((nx, ny))
                same_item_coordinates.append((nx, ny))
                visited[nx][ny] = 1
    if len(same_item_coordinates) < 3:
        return 0
    value = 0
    while same_item_coordinates:
        x, y = same_item_coordinates.popleft()
        grid[x][y] = EMPTY
        value += 1
    return value


def fill_new_items_to_grid():
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE - 1, -1, -1):
            if grid[x][y] == EMPTY:
                grid[x][y] = new_items.popleft()


dirs = ((-1, 0), (0, 1), (0, -1), (1, 0))
K, M = map(int, input().split())
grid = [list(map(int, input().split())) for _ in range(GRID_SIZE)]
new_items = deque(list(map(int, input().split())))
for _ in range(K):
    max_value, d, sy, sx = find_max_value_coordinate()
    if not max_value:
        break
    update_grid(sx, sy, d)
    cur_value = remove_used_items_from_grid()
    turn_value = 0
    while cur_value > 0:
        turn_value += cur_value
        fill_new_items_to_grid()
        cur_value = remove_used_items_from_grid()
    print(turn_value, end=' ')
