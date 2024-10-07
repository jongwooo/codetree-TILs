from collections import deque

EMPTY = 0
ROCK = 1


def int_minus_one():
    return lambda k : int(k) - 1


def find_nearest_passenger():
    candidates = []
    queue = deque([(ex, ey)])
    visited = [[-1] * n for _ in range(n)]
    visited[ex][ey] = 0
    while queue:
        x, y = queue.popleft()
        if passenger_pos[x][y]:
            candidates.append((visited[x][y], x, y))
        for dx, dy in dirs:
            nx = x + dx
            ny = y + dy
            if 0 <= nx < n and 0 <= ny < n and visited[nx][ny] == -1 and road[nx][ny] != ROCK:
                queue.append((nx, ny))
                visited[nx][ny] = visited[x][y] + 1
    candidates.sort()
    return candidates[0]


def find_passenger_destination(pid):
    queue = deque([(ex, ey)])
    visited = [[-1] * n for _ in range(n)]
    visited[ex][ey] = 0
    while queue:
        x, y = queue.popleft()
        if destination_pos[x][y] == pid:
            return visited[x][y], x, y
        for dx, dy in dirs:
            nx = x + dx
            ny = y + dy
            if 0 <= nx < n and 0 <= ny < n and visited[nx][ny] == -1 and road[nx][ny] != ROCK:
                queue.append((nx, ny))
                visited[nx][ny] = visited[x][y] + 1


dirs = ((-1, 0), (0, 1), (1, 0), (0, -1))
n, m, c = map(int, input().split())
road = [list(map(int, input().split())) for _ in range(n)]
passenger_pos = [[0] * n for _ in range(n)]
destination_pos = [[0] * n for _ in range(n)]
ex, ey = map(int_minus_one(), input().split())
for pid in range(2, m + 2):
    x_s, y_s, x_e, y_e = map(int_minus_one(), input().split())
    passenger_pos[x_s][y_s] = pid
    destination_pos[x_e][y_e] = pid
passenger_cnt = m
while passenger_cnt > 0:
    # 승객을 태우러 출발지에 이동
    dist, tx, ty = find_nearest_passenger()
    if c < dist:
        break
    c -= dist
    pid = passenger_pos[tx][ty]
    passenger_pos[tx][ty] = EMPTY
    ex, ey = tx, ty
    # 승객을 태우고 목적지로 이동
    dist, tx, ty = find_passenger_destination(pid)
    if c < dist:
        break
    c += dist
    destination_pos[tx][ty] = EMPTY
    ex, ey = tx, ty
    passenger_cnt -= 1
print(c if not passenger_cnt else -1)