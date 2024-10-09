from collections import deque

INF = int(1e9)
UNLOCKED = 0
LOCKED = 1


def int_minus_one():
    return lambda k: int(k) - 1


def in_range(x, y):
    return 0 <= x < n and 0 <= y < n


def simulate():
    for pid in range(1, m + 1):
        if people_pos[pid] == (-1, -1) or people_pos[pid] == cvs_pos[pid]:
            continue
        cx, cy = cvs_pos[pid]
        step = bfs(cx, cy)
        px, py = people_pos[pid]
        dist = INF
        tx, ty = -1, -1
        for dx, dy in dirs:
            nx = px + dx
            ny = py + dy
            if in_range(nx, ny) and step[nx][ny] != -1 and step[nx][ny] < dist:
                dist = step[nx][ny]
                tx, ty = nx, ny
        people_pos[pid] = (tx, ty)
    lock_grid()
    if time > m:
        return
    enter_base_camp()


def bfs(x, y):
    queue = deque([(x, y)])
    step = [[-1] * n for _ in range(n)]
    step[x][y] = 0
    while queue:
        x, y = queue.popleft()
        for dx, dy in dirs:
            nx = x + dx
            ny = y + dy
            if in_range(nx, ny) and step[nx][ny] == -1 and locked[nx][ny] == UNLOCKED:
                queue.append((nx, ny))
                step[nx][ny] = step[x][y] + 1
    return step


def lock_grid():
    global locked
    for pid in range(1, m + 1):
        if people_pos[pid] == cvs_pos[pid]:
            cx, cy = cvs_pos[pid]
            locked[cx][cy] = LOCKED


def enter_base_camp():
    global people_pos, locked
    cx, cy = cvs_pos[time]
    step = bfs(cx, cy)
    dist = INF
    bx, by = -1, -1
    for x in range(n):
        for y in range(n):
            if step[x][y] != -1 and grid[x][y] and step[x][y] < dist:
                dist = step[x][y]
                bx, by = x, y
    people_pos[time] = (bx, by)
    locked[bx][by] = LOCKED


def is_all_people_arrived_at_cvs():
    for pid in range(1, m + 1):
        if people_pos[pid] != cvs_pos[pid]:
            return False
    return True


dirs = ((-1, 0), (0, -1), (0, 1), (1, 0))  # ↑, ←, →, ↓
n, m = map(int, input().split())
grid = [list(map(int, input().split())) for _ in range(n)]
locked = [[0] * n for _ in range(n)]
people_pos = [(-1, -1) for _ in range(m + 1)]
cvs_pos = [(-1, -1)] + [tuple(map(int_minus_one(), input().split())) for _ in range(m)]
time = 0
while True:
    time += 1
    simulate()
    if is_all_people_arrived_at_cvs():
        break
print(time)