import sys
from collections import deque


def initialize_score_sum():
    for i in range(n):
        for j in range(n):
            if score_sum[i][j] == 0:
                bfs(i, j)


def bfs(x, y):
    global score_sum
    queue = deque([(x, y)])
    number = grid[x][y]
    same_numbers = deque([(x, y)])  # 해당 칸 숫자 * 개수 계산용
    score_sum[x][y] = 1  # 방문 체크용
    while queue:
        x, y = queue.popleft()
        for dx, dy in dirs:
            nx = x + dx
            ny = y + dy
            if 0 <= nx < n and 0 <= ny < n and score_sum[nx][ny] == 0 and grid[nx][ny] == number:
                queue.append((nx, ny))
                same_numbers.append((nx, ny))
                score_sum[nx][ny] = 1
    cnt = len(same_numbers)
    while same_numbers:
        x, y = same_numbers.popleft()
        score_sum[x][y] = number * cnt


def roll_dice():
    global dice, r, c
    dr, dc = dirs[d]
    r += dr
    c += dc
    temp_dice = dice[:]
    if d == 0:  # 오른쪽
        dice = [temp_dice[left], temp_dice[right], temp_dice[top], temp_dice[bottom], temp_dice[down], temp_dice[up]]
    elif d == 1:  # 아래
        dice = [temp_dice[up], temp_dice[down], temp_dice[right], temp_dice[left], temp_dice[top], temp_dice[bottom]]
    elif d == 2:  # 왼쪽
        dice = [temp_dice[right], temp_dice[left], temp_dice[bottom], temp_dice[top], temp_dice[down], temp_dice[up]]
    else:  # 위
        dice = [temp_dice[down], temp_dice[up], temp_dice[right], temp_dice[left], temp_dice[bottom], temp_dice[top]]


def calculate_score():
    global total_score
    total_score += score_sum[r][c]


def check_direction():
    global d
    dice_bottom = dice[bottom]
    number = grid[r][c]
    if dice_bottom > number:  # 시계
        d = (d + 1) % 4
    elif dice_bottom < number:  # 반시계
        d = (d - 1) % 4
    dr, dc = dirs[d]
    nr = r + dr
    nc = c + dc
    if nr < 0 or n <= nr or nc < 0 or n <= nc:  # 격자판을 벗어난다면 반대 방향으로 반사된다
        d = (d + 2) % 4


n, m = map(int, sys.stdin.readline().split())
grid = [list(map(int, sys.stdin.readline().split())) for _ in range(n)]
top, bottom, right, left, down, up = 0, 1, 2, 3, 4, 5  # 위, 아래, 동서남북 순서
dice = [1, 6, 3, 4, 2, 5]
r, c, d = 0, 0, 0  # 초기 방향 오른쪽
dirs = ((0, 1), (1, 0), (0, -1), (-1, 0))  # 우 하 좌 상
score_sum = [[0] * n for _ in range(n)]
initialize_score_sum()
total_score = 0
for _ in range(m):
    roll_dice()
    calculate_score()
    check_direction()
print(total_score)