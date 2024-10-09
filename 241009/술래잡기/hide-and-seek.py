def int_minus_one():
    return lambda c: int(c) - 1


def in_range(x, y):
    return 0 <= x < n and 0 <= y < n


def define_seeker_path():
    global seeker_path
    in_to_out_path = []
    x, y = n // 2, n // 2
    d = 0
    move = 0
    dist = 1
    flag = False
    while True:
        for _ in range(dist):
            in_to_out_path.append((x, y, d))
            dx, dy = dirs[d]
            nx = x + dx
            ny = y + dy
            if (nx, ny) == (-1, 0):
                flag = True
                break
            x, y = nx, ny
        if flag:
            break
        d = (d + 1) % 4
        move += 1
        if move == 2:
            move = 0
            dist += 1
    seeker_path = in_to_out_path + in_to_out_path[::-1][1:len(in_to_out_path) - 1]


def distance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)


def runaways_move():
    global runaway_pos, runaway_d
    for pid in range(m):
        if tagged[pid]:
            continue
        rx, ry = runaway_pos[pid]
        sx, sy, _ = seeker_path[seeker_pos_idx]
        if distance(rx, ry, sx, sy) > 3:
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


def find_and_tag_runaways():
    global tagged
    sx, sy, sd = seeker_path[seeker_pos_idx]
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
seeker_path = []
define_seeker_path()
seeker_pos_idx = 0
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
    seeker_pos_idx += (seeker_pos_idx + 1) % len(seeker_path)
    tagged_cnt = find_and_tag_runaways()
    score += turn * tagged_cnt
print(score)