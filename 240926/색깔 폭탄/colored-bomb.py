from collections import deque

EMPTY = -2
STONE = -1
RED_BOOM = 0


def find_and_eliminate_max_size_boom_bundle():
    global grid, score
    candidates = []
    visited = [[False] * n for _ in range(n)]
    for x in range(n):
        for y in range(n):
            if not visited[x][y] and grid[x][y] >= 0:
                red_cnt, bundle = bfs(x, y, visited)
                if len(bundle) > 1:
                    rx, ry = find_reference_point(bundle)
                    candidates.append((-len(bundle), red_cnt, -rx, ry, bundle))
    if not candidates:
        return False
    candidates.sort()
    c, _, _, _, bundle = candidates[0]
    for x, y in bundle:
        grid[x][y] = EMPTY
    score += c * c
    return True


def find_reference_point(bundle):
    bundle.sort(key=lambda k: (-k[0], k[1]))
    for x, y in bundle:
        if grid[x][y] == RED_BOOM:
            continue
        return x, y


def bfs(sx, sy, visited):
    queue = deque([(sx, sy)])
    temp = [[False] * n for _ in range(n)]
    temp[sx][sy] = True
    color = grid[sx][sy]
    bundle = []
    red_cnt = 0
    while queue:
        x, y = queue.popleft()
        bundle.append((x, y))
        if grid[x][y] == RED_BOOM:
            red_cnt += 1
        for dx, dy in dirs:
            nx = x + dx
            ny = y + dy
            if 0 <= nx < n and 0 <= ny < n and grid[nx][ny] != EMPTY and grid[nx][ny] != STONE and not temp[nx][ny] \
                    and (grid[nx][ny] == RED_BOOM or grid[nx][ny] == color):
                queue.append((nx, ny))
                temp[nx][ny] = True
    for i in range(n):
        for j in range(n):
            if grid[i][j] != RED_BOOM and temp[i][j]:
                visited[i][j] = temp[i][j]
    return red_cnt, bundle


def rotate():
    global grid
    grid = list(map(list, reversed(list(zip(*grid)))))


def gravity():
    global grid
    for y in range(n):
        for x in range(n - 1, -1, -1):
            cur_x = x
            while cur_x + 1 < n and grid[cur_x][y] != STONE and grid[cur_x + 1][y] == EMPTY:
                grid[cur_x + 1][y], grid[cur_x][y] = grid[cur_x][y], grid[cur_x + 1][y]
                cur_x += 1


n, m = map(int, input().split())
grid = [list(map(int, input().split())) for _ in range(n)]
dirs = ((1, 0), (0, -1), (-1, 0), (0, 1))
score = 0
while True:
    if not find_and_eliminate_max_size_boom_bundle():
        break
    gravity()
    rotate()
    gravity()
print(score)