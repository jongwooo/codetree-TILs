import heapq
from collections import deque


def rotate_90(sx, sy):
    global grid
    temp = [[0] * 5 for _ in range(5)]
    for x in range(sx, sx + 3):
        for y in range(sy, sy + 3):
            ox = x - sx
            oy = y - sy
            rx = oy
            ry = 3 - ox - 1
            temp[sx + rx][sy + ry] = grid[x][y]
    for x in range(sx, sx + 3):
        for y in range(sy, sy + 3):
            grid[x][y] = temp[x][y]


def find_max_value_coordinate():
    candidates = []
    for sx in range(3):
        for sy in range(3):
            for d in range(4):
                rotate_90(sx, sy)
                if d == 3:
                    break
                visited = [[False] * 5 for _ in range(5)]
                cur_value = 0
                for x in range(5):
                    for y in range(5):
                        if not visited[x][y]:
                            cur_value += bfs1(x, y, visited)
                heapq.heappush(candidates, (-cur_value, d, sy, sx))
    return heapq.heappop(candidates)


def bfs1(x, y, visited):
    queue = deque([(x, y)])
    visited[x][y] = True
    number = grid[x][y]
    cnt = 1
    while queue:
        x, y = queue.popleft()
        for dx, dy in dirs:
            nx = x + dx
            ny = y + dy
            if 0 <= nx < 5 and 0 <= ny < 5 and not visited[nx][ny] and grid[nx][ny] == number:
                queue.append((nx, ny))
                visited[nx][ny] = True
                cnt += 1
    if cnt < 3:
        return 0
    return cnt


def update_grid(d, sx, sy):
    global grid
    for _ in range(d + 1):
        rotate_90(sx, sy)


def remove_used_items():
    cnt = 0
    visited = [[False] * 5 for _ in range(5)]
    for x in range(5):
        for y in range(5):
            if not visited[x][y]:
                cnt += bfs2(x, y, visited)
    return cnt


def bfs2(x, y, visited):
    global grid
    queue = deque([(x, y)])
    visited[x][y] = True
    number = grid[x][y]
    same_numbers = deque([(x, y)])
    while queue:
        x, y = queue.popleft()
        for dx, dy in dirs:
            nx = x + dx
            ny = y + dy
            if 0 <= nx < 5 and 0 <= ny < 5 and not visited[nx][ny] and grid[nx][ny] == number:
                queue.append((nx, ny))
                same_numbers.append((nx, ny))
                visited[nx][ny] = True
    if len(same_numbers) < 3:
        return 0
    cnt = 0
    while same_numbers:
        x, y = same_numbers.popleft()
        grid[x][y] = 0
        cnt += 1
    return cnt


def fill_next_items_to_empty_space():
    global grid
    for y in range(5):
        for x in range(4, -1, -1):
            if grid[x][y] == 0:
                grid[x][y] = next_items.popleft()


K, M = map(int, input().split())
grid = [list(map(int, input().split())) for _ in range(5)]
next_items = deque(list(map(int, input().split())))
dirs = ((-1, 0), (0, 1), (0, -1), (1, 0))
for _ in range(K):
    value, d, sy, sx = find_max_value_coordinate()
    if value == 0:
        break
    update_grid(d, sx, sy)
    cur_value = remove_used_items()
    item_values_sum = 0
    while cur_value > 0:
        item_values_sum += cur_value
        fill_next_items_to_empty_space()
        cur_value = remove_used_items()
    print(item_values_sum, end=' ')
