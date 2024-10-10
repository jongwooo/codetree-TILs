from collections import deque

EMPTY = 0
HEAD = 1
BODY = 2
TAIL = 3
LINE = 4
MIN_TEAM_ID = 5


def in_range(x, y):
    return 0 <= x < n and 0 <= y < n


def initialize_teams():
    global teams
    visited = [[0] * n for _ in range(n)]
    team_id = MIN_TEAM_ID
    for x in range(n):
        for y in range(n):
            if grid[x][y] == HEAD and not visited[x][y]:
                bfs(x, y, visited, team_id)
                team_id += 1


def bfs(hx, hy, visited, team_id):
    global grid, teams
    queue = deque([(hx, hy)])
    team = deque([(hx, hy)])
    visited[hx][hy] = 1
    grid[hx][hy] = team_id
    while queue:
        x, y = queue.popleft()
        for dx, dy in head_dirs:
            nx = x + dx
            ny = y + dy
            if in_range(nx, ny) and not visited[nx][ny]:
                if grid[nx][ny] == BODY or ((hx, hy) != (x, y) and grid[nx][ny] == TAIL):
                    queue.append((nx, ny))
                    team.append((nx, ny))
                    visited[nx][ny] = 1
                    grid[nx][ny] = team_id
    teams[team_id] = team


def heads_move():
    global grid, teams
    for team in teams.values():
        tx, ty = team.pop()
        team_id = grid[tx][ty]
        grid[tx][ty] = LINE
        hx, hy = team[0]
        for dx, dy in head_dirs:
            nx = hx + dx
            ny = hy + dy
            if in_range(nx, ny) and grid[nx][ny] == LINE:
                team.appendleft((nx, ny))
                grid[nx][ny] = team_id
                break


def throw_ball(r):
    global score
    d = (r // n) % 4
    offset = r % n
    if d == 0:
        x, y = offset, 0
    elif d == 1:
        x, y = n - 1, offset
    elif d == 2:
        x, y = n - 1 - offset, n - 1
    else:
        x, y = 0, n - 1 - offset
    dx, dy = ball_dirs[d]
    for _ in range(n):
        if in_range(x, y) and grid[x][y] >= MIN_TEAM_ID:
            team_id = grid[x][y]
            score += (teams[team_id].index((x, y)) + 1) ** 2
            teams[team_id].reverse()
            break
        x += dx
        y += dy


head_dirs = ((-1, 0), (0, 1), (1, 0), (0, -1))
ball_dirs = ((0, 1), (-1, 0), (0, -1), (1, 0))
n, m, k = map(int, input().split())
grid = [list(map(int, input().split())) for _ in range(n)]
teams = dict()
initialize_teams()
score = 0
for r in range(k):
    heads_move()
    throw_ball(r)
print(score)