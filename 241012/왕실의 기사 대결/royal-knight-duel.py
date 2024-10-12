EMPTY = 0
TRAP = 1
WALL = 2


def reach_the_wall(pid, d):
    r, c, h, w, _ = knights[pid]
    dr, dc = knights_dirs[d]
    for i in range(h):
        for j in range(w):
            if board[r + i + dr][c + j + dc] == WALL:
                return True
    return False


def knights_move(pid, d):
    stack = [pid]
    interaction_set = interaction(pid, d)
    while interaction_set:
        next_interaction_set = set()
        for next_pid in interaction_set:
            if reach_the_wall(next_pid, d):
                return
            if next_pid not in stack:
                stack.append(next_pid)
            next_interaction_set.update(interaction(next_pid, d))
        interaction_set = next_interaction_set
    while stack:
        p = stack.pop()
        knight_move(p, d)
        if p != pid:
            check_trap(p)


def knight_move(pid, d):
    global knights, knights_board
    r, c, h, w, k = knights[pid]
    dr, dc = knights_dirs[d]
    for i in range(h):
        for j in range(w):
            knights_board[r + i][c + j] = EMPTY
    for i in range(h):
        for j in range(w):
            knights_board[r + i + dr][c + j + dc] = pid
    knights[pid] = (r + dr, c + dc, h, w, k)


def interaction(pid, d):
    global knights, knights_board
    r, c, h, w, _ = knights[pid]
    dr, dc = knights_dirs[d]
    interaction_set = set()
    for i in range(h):
        for j in range(w):
            nr = r + i + dr
            nc = c + j + dc
            if knights_board[nr][nc] != pid and knights_board[nr][nc] != EMPTY:
                interaction_set.add(knights_board[nr][nc])
    return interaction_set


def check_trap(pid):
    global game_over, damages
    r, c, h, w, k = knights[pid]
    for i in range(h):
        for j in range(w):
            if board[r + i][c + j] == TRAP:
                damages[pid] += 1
                k -= 1
            if k == 0:
                delete_knight_from_board(pid)
                return
    knights[pid] = (r, c, h, w, k)


def delete_knight_from_board(pid):
    global knights_board, damages
    r, c, h, w, _ = knights[pid]
    game_over[pid] = True
    damages[pid] = 0
    del knights[pid]
    for i in range(h):
        for j in range(w):
            knights_board[r + i][c + j] = EMPTY


knights_dirs = ((-1, 0), (0, 1), (1, 0), (0, -1))  # 위쪽, 오른쪽, 아래쪽, 왼쪽
L, N, Q = map(int, input().split())
board = [[WALL] * (L + 2)] + [[WALL] + list(map(int, input().split())) + [WALL] for _ in range(L)] + [[WALL] * (L + 2)]
knights = dict()
knights_board = [[EMPTY] * (L + 2) for _ in range(L + 2)]
game_over = [False] * (N + 1)
damages = [0] * (N + 1)
for pid in range(1, N + 1):
    r, c, h, w, k = map(int, input().split())
    knights[pid] = (r, c, h, w, k)
    for i in range(h):
        for j in range(w):
            knights_board[r + i][c + j] = pid
for _ in range(Q):
    pid, d = map(int, input().split())
    if game_over[pid]:
        continue
    if reach_the_wall(pid, d):
        continue
    knights_move(pid, d)
print(sum(damages))