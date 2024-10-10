from collections import deque

TOP, BOTTOM, RIGHT, LEFT, DOWN, UP = 0, 1, 2, 3, 4, 5


def in_range(x, y):
    return 0 <= x < n and 0 <= y < n


def initialize_score_sum():
    global score_sum
    for x in range(n):
        for y in range(n):
            if not score_sum[x][y]:
                bfs(x, y)


def bfs(x, y):
    queue = deque([(x, y)])
    same_num_pos = deque([(x, y)])
    num = grid[x][y]
    score_sum[x][y] = 1
    while queue:
        x, y = queue.popleft()
        for dx, dy in dirs:
            nx = x + dx
            ny = y + dy
            if in_range(nx, ny) and not score_sum[nx][ny] and grid[nx][ny] == num:
                queue.append((nx, ny))
                same_num_pos.append((nx, ny))
                score_sum[nx][ny] = 1
    cnt = len(same_num_pos)
    while same_num_pos:
        x, y = same_num_pos.popleft()
        score_sum[x][y] = num * cnt


def roll_dice():
    global dice, dice_x, dice_y, dice_d
    dx, dy = dirs[dice_d]
    nx = dice_x + dx
    ny = dice_y + dy
    if not in_range(nx, ny):
        nx = dice_x - dx
        ny = dice_y - dy
        dice_d = (dice_d + 2) % 4
    dice_x, dice_y = nx, ny
    if dice_d == 0:
        dice = [dice[LEFT], dice[RIGHT], dice[TOP], dice[BOTTOM], dice[DOWN], dice[UP]]
    elif dice_d == 1:
        dice = [dice[UP], dice[DOWN], dice[RIGHT], dice[LEFT], dice[TOP], dice[BOTTOM]]
    elif dice_d == 2:
        dice = [dice[RIGHT], dice[LEFT], dice[BOTTOM], dice[TOP], dice[DOWN], dice[UP]]
    elif dice_d == 3:
        dice = [dice[DOWN], dice[UP], dice[RIGHT], dice[LEFT], dice[BOTTOM], dice[TOP]]


def calculate_score():
    global total_score
    total_score += score_sum[dice_x][dice_y]


def check_direction():
    global dice_d
    bottom_num = dice[BOTTOM]
    if bottom_num > grid[dice_x][dice_y]:
        dice_d = (dice_d + 1) % 4
    elif bottom_num < grid[dice_x][dice_y]:
        dice_d = (dice_d - 1) % 4


dirs = ((0, 1), (1, 0), (0, -1), (-1, 0))
n, m = map(int, input().split())
grid = [list(map(int, input().split())) for _ in range(n)]
dice = [1, 6, 3, 4, 2, 5]
dice_x, dice_y = 0, 0
dice_d = 0
score_sum = [[0] * n for _ in range(n)]
initialize_score_sum()
total_score = 0
for _ in range(m):
    roll_dice()
    calculate_score()
    check_direction()
print(total_score)