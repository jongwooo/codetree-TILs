EMPTY = 0
RUDOLPH = -1


def in_board(x, y):
    return 0 < x <= N and 0 < y <= N


def distance(r1, c1, r2, c2):
    return (r1 - r2) ** 2 + (c1 - c2) ** 2


def turn(t):
    rudolph_move(t)
    if santa_cnt == 0:
        return
    for pn in range(1, P + 1):
        if not alive[pn]:
            continue
        if panic_time[pn] < t:
            santa_move(t, pn)
        if santa_cnt == 0:
            return
    for pn in range(1, P + 1):
        if alive[pn]:
            score[pn] += 1


def rudolph_move(t):
    global rr, rc, board
    candidates = []
    for pn in range(1, P + 1):
        if not alive[pn]:
            continue
        sr, sc = santa[pn]
        dist = distance(rr, rc, sr, sc)
        candidates.append((dist, -sr, -sc))
    candidates.sort()
    _, target_sr, target_sc = candidates[0]
    target_sr, target_sc = -target_sr, -target_sc
    board[rr][rc] = EMPTY
    dr, dc = 0, 0
    if target_sr > rr:
        dr = 1
    elif target_sr < rr:
        dr = -1
    if target_sc > rc:
        dc = 1
    elif target_sc < rc:
        dc = -1
    nr = rr + dr
    nc = rc + dc
    if board[nr][nc] != EMPTY:
        crush_rudolph_to_santa(t, nr, nc, dr, dc)
    board[nr][nc] = RUDOLPH
    rr, rc = nr, nc


def crush_rudolph_to_santa(t, sr, sc, dr, dc):
    global board, santa, santa_cnt, panic_time, alive, score
    pn = board[sr][sc]
    board[sr][sc] = EMPTY
    panic_time[pn] = t + 1
    score[pn] += C
    nsr = sr + dr * C
    nsc = sc + dc * C
    if not in_board(nsr, nsc):
        del santa[pn]
        alive[pn] = 0
        santa_cnt -= 1
        return
    if board[nsr][nsc] != EMPTY:
        interaction(nsr, nsc, dr, dc)
    board[nsr][nsc] = pn
    santa[pn] = (nsr, nsc)


def santa_move(t, pn):
    global board, santa
    sr, sc = santa[pn]
    cur_dist = distance(rr, rc, sr, sc)
    candidates = []
    for d in range(4):
        dr, dc = santa_dirs[d]
        nsr = sr + dr
        nsc = sc + dc
        dist = distance(rr, rc, nsr, nsc)
        if in_board(nsr, nsc) and (board[nsr][nsc] == EMPTY or board[nsr][nsc] == RUDOLPH) and dist < cur_dist:
            candidates.append((dist, d, nsr, nsc))
    if not candidates:
        return
    candidates.sort()
    _, d, nsr, nsc = candidates[0]
    board[sr][sc] = EMPTY
    if board[nsr][nsc] == RUDOLPH:
        crush_santa_to_rudolph(t, pn, d)
    else:
        board[nsr][nsc] = pn
        santa[pn] = (nsr, nsc)


def crush_santa_to_rudolph(t, pn, d):
    global board, santa, santa_cnt, panic_time, alive, score
    panic_time[pn] = t + 1
    score[pn] += D
    dr, dc = santa_dirs[d]
    nsr = rr - dr * D
    nsc = rc - dc * D
    if not in_board(nsr, nsc):
        del santa[pn]
        alive[pn] = 0
        santa_cnt -= 1
        return
    if board[nsr][nsc] != EMPTY:
        interaction(nsr, nsc, -dr, -dc)
    board[nsr][nsc] = pn
    santa[pn] = (nsr, nsc)


def interaction(r, c, dr, dc):
    global board, santa, santa_cnt, alive
    pn = board[r][c]
    board[r][c] = EMPTY
    nsr = r + dr
    nsc = c + dc
    if not in_board(nsr, nsc):
        del santa[pn]
        alive[pn] = 0
        santa_cnt -= 1
        return
    if board[nsr][nsc] != EMPTY:
        interaction(nsr, nsc, dr, dc)
    board[nsr][nsc] = pn
    santa[pn] = (nsr, nsc)


santa_dirs = ((-1, 0), (0, 1), (1, 0), (0, -1))  # 상 우 하 좌
N, M, P, C, D = map(int, input().split())
board = [[EMPTY] * (N + 1) for _ in range(N + 1)]
rr, rc = map(int, input().split())
board[rr][rc] = RUDOLPH
santa = dict()
santa_cnt = P
panic_time = [0] * (P + 1)
alive = [0] + [1] * P
score = [0] * (P + 1)
for _ in range(P):
    pn, sr, sc = map(int, input().split())
    board[sr][sc] = pn
    santa[pn] = (sr, sc)
for k in range(1, M + 1):
    turn(k)
    if santa_cnt == 0:
        break
print(*score[1:])