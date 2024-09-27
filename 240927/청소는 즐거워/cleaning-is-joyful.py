def wipe_floor():
    global dust_out
    x, y = n // 2, n // 2
    d = 0
    move = 0
    dist = 1
    while True:
        dx, dy = move_dirs[d]
        for _ in range(dist):
            nx = x + dx
            ny = y + dy
            if (nx, ny) == (0, -1):
                return
            clean_dust(d, nx, ny)
            x, y = nx, ny
        d = (d + 1) % 4
        move += 1
        if move == 2:
            move = 0
            dist += 1


def clean_dust(d, x, y):
    global grid, dust_out
    dust = grid[x][y]
    grid[x][y] = 0
    left = dust
    for i in range(5):
        for j in range(5):
            scattered_dust = int(dust * proportions[d][i][j])
            left -= scattered_dust
            nx = x + i - 2
            ny = y + j - 2
            if 0 <= nx < n and 0 <= ny < n:
                grid[nx][ny] += scattered_dust
            else:
                dust_out += scattered_dust
    ax = x + alphas[d][0] - 2
    ay = y + alphas[d][1] - 2
    if 0 <= ax < n and 0 <= ay < n:
        grid[ax][ay] += left
    else:
        dust_out += left


def rotate(p):
    return list(reversed(list(zip(*p))))


p0 = [
    [0, 0, 0.02, 0, 0],
    [0, 0.1, 0.07, 0.01, 0],
    [0.05, 0, 0, 0, 0],
    [0, 0.1, 0.07, 0.01, 0],
    [0, 0, 0.02, 0, 0]
]
p1 = rotate(p0)
p2 = rotate(p1)
p3 = rotate(p2)
proportions = (p0, p1, p2, p3)
alphas = ((2, 1), (3, 2), (2, 3), (1, 2))
n = int(input())
grid = [list(map(int, input().split())) for _ in range(n)]
move_dirs = ((0, -1), (1, 0), (0, 1), (-1, 0))  # 왼쪽 - 아래쪽 - 오른쪽 - 위쪽
dust_out = 0
wipe_floor()
print(dust_out)