import sys


def initialize_in_to_out():  # 안에서 밖으로의 술래 방향 초기화
    global in_to_out
    dirs = ((-1, 0), (0, 1), (1, 0), (0, -1))
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


def initialize_out_to_in():  # 밖에서 안으로의 술래 방향 초기화
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


def distance_from_tagger(fx, fy):
    return abs(tx - fx) + abs(ty - fy)  # 두 사람 간의 거리는 |x1 - x2| + |y1 - y2|


def fugitive_move():
    global fugitives
    for fid in range(len(fugitives)):  # 모든 도망자에 대해
        if tagged[fid]:  # 만약 술래에게 잡혔다면
            continue  # 건너뛴다
        x, y = fugitives[fid]
        d_type, cur_d = fugitives_info[fid]
        if distance_from_tagger(x, y) <= 3:  # 술래와의 거리가 3 이하인 도망자들은 1턴 동안 움직인다
            nx, ny = x, y  # 현재 바라보고 있는 방향으로 1칸 움직인다 했을 때
            if d_type == 1:  # 좌우 움직임
                ny += fugitives_dirs[cur_d]
            elif d_type == 2:  # 상하 움직임
                nx += fugitives_dirs[cur_d]
            if nx < 0 or n <= nx or ny < 0 or n <= ny:  # 격자를 벗어나는 경우
                cur_d = 1 - cur_d  # 방향을 반대로 틀어준다
                fugitives_info[fid] = (d_type, cur_d)  # 방향 정보를 갱신한다
                nx, ny = x, y  # x, y로 다시 초기화
                if d_type == 1:  # 좌우 움직임
                    ny += fugitives_dirs[cur_d]  # 반대로 움직임
                elif d_type == 2:  # 상하 움직임
                    nx += fugitives_dirs[cur_d]  # 반대로 움직임
            if (tx, ty) == (nx, ny):  # 움직이려는 칸에 술래가 있는 경우
                continue  # 움직이지 않는다
            else:  # 움직이려는 칸에 술래가 없는 경우
                fugitives[fid] = (nx, ny)  # 해당 칸으로 이동한다


def tagger_move():
    global tx, ty, in_out
    if in_out:  # 안에서 밖으로
        td = in_to_out[tx][ty]
    else:  # 밖에서 안으로
        td = out_to_in[tx][ty]
    dx, dy = tagger_dirs[td]
    tx += dx
    ty += dy
    if (tx, ty) == (0, 0):
        in_out = False
    elif (tx, ty) == (n // 2, n // 2):
        in_out = True


def tag_fugitives(turn):
    global tagged, score
    tagged_cnt = 0
    if in_out:
        td = in_to_out[tx][ty]
    else:
        td = out_to_in[tx][ty]
    x, y = tx, ty
    dx, dy = tagger_dirs[td]
    for _ in range(3):
        if (x, y) in fugitives and (x, y) not in trees:  # 범위 내에 도망자가 있고, 그 칸에 나무가 없으면
            fid = fugitives.index((x, y))
            tagged[fid] = True  # 도망자를 태그한다
            tagged_cnt += 1
        x += dx
        y += dy
    score += tagged_cnt * turn


n, m, h, k = map(int, sys.stdin.readline().split())
in_to_out = [[0] * n for _ in range(n)]
out_to_in = [[-1] * n for _ in range(n)]
initialize_in_to_out()
initialize_out_to_in()
tx, ty = n // 2, n // 2
in_out = True
fugitives = []
fugitives_info = []
tagged = [False] * m
for _ in range(m):
    x, y, d_type = map(int, sys.stdin.readline().split())
    fugitives.append((x - 1, y - 1))  # x, y 1칸 만큼 보정
    fugitives_info.append((d_type, 0))  # d_type 정보와 현재 방향 정보
trees = []
for _ in range(h):
    x, y = map(int, sys.stdin.readline().split())
    trees.append((x - 1, y - 1))  # x, y 1칸 만큼 보정
tagger_dirs = ((-1, 0), (0, 1), (1, 0), (0, -1))
fugitives_dirs = (1, -1)
score = 0
for t in range(1, k + 1):
    fugitive_move()  # m명의 도망자가 먼저 동시에 움직인다
    tagger_move()  # 술래가 움직인다
    tag_fugitives(t)  # 술래가 범위 내 도망자를 찾는다
print(score)