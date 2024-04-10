import sys
from collections import deque


def initialize_teams():
    team_num = 5  # 팀 수가 5 이하이기 때문에 가능한 팀 번호는 5 ~ 9 이다
    for i in range(n):
        for j in range(n):
            if grid[i][j] == 1 and not visited[i][j]:
                bfs(i, j, team_num)  # 팀 번호로 변경
                team_num += 1


def bfs(sx, sy, team_num):
    global grid, visited, teams
    queue = deque([(sx, sy)])
    team = deque([(sx, sy)])  # 팀 정보 저장
    grid[sx][sy] = team_num
    visited[sx][sy] = 1
    while queue:
        x, y = queue.popleft()
        for dx, dy in dirs:
            nx = x + dx
            ny = y + dy
            if 0 <= nx < n and 0 <= ny < n and not visited[nx][ny]:
                if grid[nx][ny] == 2 or ((sx, sy) != (x, y) and grid[nx][ny] == 3):  # 몸통 또는 꼬리인 경우
                    queue.append((nx, ny))
                    team.append((nx, ny))
                    visited[nx][ny] = 1
                    grid[nx][ny] = team_num
    teams[team_num] = team


def head_move():
    global grid, teams
    for team in teams.values():
        ex, ey = team.pop()  # 꼬리 좌표 삭제
        grid[ex][ey] = 4  # 이동 경로(4)로 변경
        sx, sy = team[0]  # 머리 좌표
        for dx, dy in dirs:
            nx = sx + dx
            ny = sy + dy
            if 0 <= nx < n and 0 <= ny < n and grid[nx][ny] == 4:
                team.appendleft((nx, ny))  # (nx, ny)가 머리가 된다
                grid[nx][ny] = grid[sx][sy]  # 팀 번호로 변경
                break


def catch_ball(r):
    global score
    d = (r // n) % 4
    offset = r % n
    if d == 0:
        cx, cy = offset, 0
    elif d == 1:
        cx, cy = n - 1, offset
    elif d == 2:
        cx, cy = n - 1 - offset, n - 1
    else:
        cx, cy = 0, n - 1 - offset
    for _ in range(n):
        if 0 <= cx < n and 0 <= cy < n and grid[cx][cy] > 4:
            team_num = grid[cx][cy]
            score += (teams[team_num].index((cx, cy)) + 1) ** 2  # 머리 기준 k번째 이면 k의 제곱이 점수가 된다
            teams[team_num].reverse()  # 방향 바뀜
            break
        cx += dx[d]
        cy += dy[d]


n, m, k = map(int, sys.stdin.readline().split())
grid = [list(map(int, sys.stdin.readline().split())) for _ in range(n)]
visited = [[0] * n for _ in range(n)]
dirs = ((-1, 0), (1, 0), (0, -1), (0, 1))
dx = (0, -1, 0, 1)
dy = (1, 0, -1, 0)
teams = {}
initialize_teams()
score = 0
for r in range(k):
    head_move()
    catch_ball(r)
print(score)