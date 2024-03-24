from collections import deque


def is_all_passed():
    for i in range(1, m + 1):
        if people[i] != cvs[i]:
            return False
    return True


def bfs(sx, sy):
    for i in range(n):
        for j in range(n):
            visited[i][j] = False
            step[i][j] = 0
    queue = deque([(sx, sy)])
    visited[sx][sy] = True
    while queue:
        x, y = queue.popleft()
        for dx, dy in dirs:
            nx = x + dx
            ny = y + dy
            if 0 <= nx < n and 0 <= ny < n and not visited[nx][ny] and lock[nx][ny] == 0:
                visited[nx][ny] = True
                step[nx][ny] = step[x][y] + 1
                queue.append((nx, ny))


def lock_board():
    for i in range(1, m + 1):
        if people[i] == cvs[i]:
            px, py = people[i]
            lock[px][py] = 1


def enter_base_camp(time):
    global m, n, dirs, board, people
    cx, cy = cvs[time]
    bfs(cx, cy)
    dist = int(1e9)
    bx, by = -1, -1
    for i in range(n):
        for j in range(n):
            if visited[i][j] and board[i][j] == 1 and dist > step[i][j]:
                dist = step[i][j]
                bx, by = i, j
    people[time] = (bx, by)
    lock[bx][by] = 1


def simulate():
    for i in range(1, m + 1):
        if people[i] == (-1, -1) or people[i] == cvs[i]:
            continue
        cx, cy = cvs[i]
        bfs(cx, cy)
        px, py = people[i]
        dist = int(1e9)
        tx, ty = -1, -1
        for dx, dy in dirs:
            nx = px + dx
            ny = py + dy
            if 0 <= nx < n and 0 <= ny < n and visited[nx][ny] and dist > step[nx][ny]:
                dist = step[nx][ny]
                tx, ty = nx, ny
        people[i] = (tx, ty)
    lock_board()
    if time > m:
        return
    enter_base_camp(time)


dirs = [(-1, 0), (0, -1), (0, 1), (1, 0)]
n, m = map(int, input().split())
board = []
for _ in range(n):
    board.append(list(map(int, input().split())))
lock = [[0] * n for _ in range(n)]
people = [(-1, -1) for _ in range(m + 1)]
cvs = [(-1, -1)]
visited = [[False] * n for _ in range(n)]
step = [[0] * n for _ in range(n)]
for _ in range(m):
    cx, cy = map(int, input().split())
    cvs.append((cx - 1, cy - 1))
time = 0
while True:
    time += 1
    simulate()
    if is_all_passed():
        break
print(time)