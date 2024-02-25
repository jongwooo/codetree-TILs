import heapq


def in_board(nx, ny):
    return 0 < nx < N + 1 and 0 < ny < N + 1


def distance(r1, c1, r2, c2):
    return (r1 - r2) ** 2 + (c1 - c2) ** 2


def interaction(nx, ny, dx, dy):
    global player_cnt
    origin_player_id = board[nx][ny]
    origin_player_loc = player[origin_player_id]
    opx, opy = origin_player_loc
    nx = opx + dx
    ny = opy + dy
    if not in_board(nx, ny):
        del player[origin_player_id]
        player_cnt -= 1
        game_over[origin_player_id] = True
        return
    if board[nx][ny] > 0:
        interaction(nx, ny, dx, dy)
    board[nx][ny] = origin_player_id
    player[origin_player_id] = (nx, ny)


def crush_player_to_rudolph(t, pid, d):
    global board, rudolph_loc, player_score, game_over, player_cnt
    px, py = player[pid]
    nx, ny = rudolph_loc
    player_score[pid] += D
    panic_time[pid] = t + 1
    dx = -pdxs[d]
    dy = -pdys[d]
    nx = nx + dx * D
    ny = ny + dy * D
    if not in_board(nx, ny):
        board[px][py] = 0
        del player[pid]
        player_cnt -= 1
        game_over[pid] = True
        return
    if board[nx][ny] > 0:
        interaction(nx, ny, dx, dy)
    player[pid] = (nx, ny)
    board[px][py] = 0
    board[nx][ny] = pid


def player_move(t, pid):
    global board, rudolph_loc
    rx, ry = rudolph_loc
    px, py = player[pid]
    possible_loc = []
    cur_dis = distance(px, py, rx, ry)
    for i in range(4):
        nx = px + pdxs[i]
        ny = py + pdys[i]
        if in_board(nx, ny) and board[nx][ny] <= 0:
            dis = distance(nx, ny, rx, ry)
            if dis < cur_dis:
                priority = [dis, i, nx, ny]
                heapq.heappush(possible_loc, priority)
    if len(possible_loc) == 0:
        return
    dis, i, nx, ny = heapq.heappop(possible_loc)
    board[px][py] = 0
    if (nx, ny) == (rx, ry):
        crush_player_to_rudolph(t, pid, i)
    else:
        board[nx][ny] = pid
        player[pid] = (nx, ny)


def crush_rudolph_to_player(t, rx, ry, d):
    global board, rudolph_loc, player_score, game_over, player_cnt
    pid = board[rx][ry]
    player_score[pid] += C
    panic_time[pid] = t + 1
    px, py = player[pid]
    nx, ny = px, py
    dx = d[0]
    dy = d[1]
    nx = nx + dx * C
    ny = ny + dy * C
    if not in_board(nx, ny):
        board[px][py] = 0
        del player[pid]
        player_cnt -= 1
        game_over[pid] = True
        return
    if board[nx][ny] > 0:
        interaction(nx, ny, dx, dy)
    player[pid] = (nx, ny)
    board[px][py] = 0
    board[nx][ny] = pid


def rudolph_move(t):
    global board, rudolph_loc
    rx, ry = rudolph_loc
    nearest_x, nearest_y, nearest_pid = 10_001, 10_001, 0
    for pid in range(1, P + 1):
        if game_over[pid]:
            continue
        px, py = player[pid]
        nearest_dis = [distance(rx, ry, nearest_x, nearest_y), [-nearest_x, -nearest_y]]
        pid_dis = [distance(rx, ry, px, py), [-px, -py]]
        if pid_dis < nearest_dis:
            nearest_x, nearest_y = player[pid]
            nearest_pid = pid
    if nearest_pid:
        dir_x = 0
        if nearest_x > rx:
            dir_x = 1
        elif nearest_x < rx:
            dir_x = -1
        dir_y = 0
        if nearest_y > ry:
            dir_y = 1
        elif nearest_y < ry:
            dir_y = -1
        rudolph_loc = [rx + dir_x, ry + dir_y]
        board[rx][ry] = 0
        d = [dir_x, dir_y]
        nx, ny = rudolph_loc
        px, py = player[nearest_pid]
        if (px, py) == (nx, ny) or board[nx][ny] != 0:
            crush_rudolph_to_player(t, nx, ny, d)
        board[nx][ny] = -1
        rudolph_loc = [nx, ny]


def turn(t):
    rudolph_move(t)
    if player_cnt == 0:
        return
    for pid in range(1, P + 1):
        if game_over[pid]:
            continue
        if panic_time[pid] < t:
            player_move(t, pid)
        if player_cnt == 0:
            return
    for pid in player:
        player_score[pid] += 1


N, M, P, C, D = map(int, input().split())
rudolph_loc = list(map(int, input().split()))
board = [[0] * (N + 1) for _ in range(N + 1)]
board[rudolph_loc[0]][rudolph_loc[1]] = -1
player = {}
player_cnt = P
player_score = [0] * (P + 1)
panic_time = [0] * (P + 1)
game_over = [True] * (P + 1)
pdxs = [-1, 0, 1, 0]
pdys = [0, 1, 0, -1]
for _ in range(P):
    pn, pr, pc = map(int, input().split())
    board[pr][pc] = pn
    player[pn] = (pr, pc)
    game_over[pn] = False
for k in range(1, M + 1):
    turn(k)
    if player_cnt == 0:
        break
print(*player_score[1:])