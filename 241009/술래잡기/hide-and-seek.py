def int_minus_one():
    return lambda c: int(c) - 1


def in_range(x, y):
    return 0 <= x < n and 0 <= y < n


def distance_from_seeker(x, y):
    return abs(sx - x) + abs(sy - y)


def initialize_in_to_out():
    global in_to_out
    x, y = n // 2, n // 2
    dist = 1
    move = 0
    d = 0
    while True:
        for _ in range(dist):
            dx, dy = dirs[d]
            x = x + dx
            y = y + dy
            in_to_out[x][y] = d
            if (x, y) == (-1, 0):
                return
        d = (d + 1) % 4
        in_to_out[x][y] = d
        move += 1
        if move == 2:
            dist += 1
            move = 0


def initialize_out_to_in():
    global out_to_in
    x, y = 0, 0
    d = 0
    for i in range(n ** 2):
        if d == 0 or d == 2:
            out_to_in[x][y] = 2 - d
        else:
            out_to_in[x][y] = d
        if d == 0:
            x += 1
            if x == n - 1 or out_to_in[x + 1][y] != -1:
                d = 1
        elif d == 1:
            y += 1
            if y == n - 1 or out_to_in[x][y + 1] != -1:
                d = 2
        elif d == 2:
            x -= 1
            if x == 0 or out_to_in[x - 1][y] != -1:
                d = 3
        elif d == 3:
            y -= 1
            if y == n - 1 or out_to_in[x][y - 1] != -1:
                d = 0


def runaways_move():
    global runaway_pos, runaway_d
    for pid in range(m):
        if tagged[pid]:
            continue
        rx, ry = runaway_pos[pid]
        if distance_from_seeker(rx, ry) > 3:
            continue
        rd = runaway_d[pid]
        dx, dy = dirs[rd]
        nx = rx + dx
        ny = ry + dy
        if not in_range(nx, ny):
            runaway_d[pid] = (rd + 2) % 4
            nx = rx - dx
            ny = ry - dy
        if (nx, ny) == (sx, sy):
            continue
        runaway_pos[pid] = (nx, ny)


def seeker_move():
    global sx, sy, in_out
    if in_out:
        sd = in_to_out[sx][sy]
    else:
        sd = out_to_in[sx][sy]
    dx, dy = dirs[sd]
    sx += dx
    sy += dy
    if (sx, sy) == (0, 0):
        in_out = False
    elif (sx, sy) == (n // 2, n // 2):
        in_out = True


def find_and_tag_runaways():
    global tagged
    if in_out:
        sd = in_to_out[sx][sy]
    else:
        sd = out_to_in[sx][sy]
    dx, dy = dirs[sd]
    tagged_cnt = 0
    for d in range(3):
        nx = sx + dx * d
        ny = sy + dy * d
        if not in_range(nx, ny):
            break
        if (nx, ny) in tree_pos:
            continue
        for pid in range(m):
            if tagged[pid]:
                continue
            if (nx, ny) == runaway_pos[pid]:
                tagged[pid] = 1
                tagged_cnt += 1
    return tagged_cnt


dirs = ((-1, 0), (0, 1), (1, 0), (0, -1))
n, m, h, k = map(int, input().split())
in_to_out = [[0] * n for _ in range(n)]
out_to_in = [[-1] * n for _ in range(n)]
initialize_in_to_out()
initialize_out_to_in()
in_out = True
sx, sy = n // 2, n // 2
runaway_pos = []
runaway_d = [0] * m
tagged = [0] * m
for pid in range(m):
    x, y, d = map(int, input().split())
    runaway_pos.append((x - 1, y - 1))
    runaway_d[pid] = d
tree_pos = [tuple(map(int_minus_one(), input().split())) for _ in range(h)]
score = 0
for turn in range(1, k + 1):
    runaways_move()
    seeker_move()
    tagged_cnt = find_and_tag_runaways()
    score += turn * tagged_cnt
print(score)