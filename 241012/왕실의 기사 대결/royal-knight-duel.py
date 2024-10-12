EMPTY = 0
TRAP = 1
WALL = 2


def reach_the_wall(pid, d):
    r, c, h, w = knights[pid]
    dr, dc = knights_dirs[d]
    for i in range(h):
        for j in range(w):
            if board[r + i + dr][c + j + dc] == WALL:
                return TRAP
    return False


def knights_move(pid, d):
    stack = [pid]
    interaction_set = interaction(pid, d)
    while interaction_set:
        next_interaction_set = set()
        for next_pid in interaction_set:
            if reach_the_wall(next_pid, d):
                return
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
    r, c, h, w = knights[pid]
    dr, dc = knights_dirs[d]
    for i in range(h):
        for j in range(w):
            knights_board[r + i][c + j] = EMPTY
    for i in range(h):
        for j in range(w):
            knights_board[r + i + dr][c + j + dc] = pid
    knights[pid] = (r + dr, c + dc, h, w)


def interaction(pid, d):
    global knights, knights_board
    r, c, h, w = knights[pid]
    dr, dc = knights_dirs[d]
    interaction_set = set()
    for i in range(h):
        for j in range(w):
            if knights_board[r + i + dr][c + j + dc] != pid and knights_board[r + i + dr][c + j + dc] != EMPTY:
                interaction_set.add(knights_board[r + i + dr][c + j + dc])
    return interaction_set


def check_trap(pid):
    global knights_stamina, damages
    r, c, h, w = knights[pid]
    for i in range(h):
        for j in range(w):
            if board[r + i][c + j] == TRAP:
                knights_stamina[pid] -= 1
                damages[pid] += 1
            if not knights_stamina[pid]:
                delete_knight_from_board(pid)
                return


def delete_knight_from_board(pid):
    global knights_board, damages
    r, c, h, w = knights[pid]
    for i in range(h):
        for j in range(w):
            knights_board[r + i][c + j] = EMPTY
    damages[pid] = 0


knights_dirs = ((-1, 0), (0, 1), (1, 0), (0, -1))  # 위쪽, 오른쪽, 아래쪽, 왼쪽
L, N, Q = map(int, input().split())
board = [[WALL] * (L + 2)] + [[WALL] + list(map(int, input().split())) + [WALL] for _ in range(L)] + [[WALL] * (L + 2)]
knights = dict()
knights_board = [[EMPTY] * (L + 2) for _ in range(L + 2)]
knights_stamina = [0] * (N + 1)
damages = [0] * (N + 1)
for pid in range(1, N + 1):
    r, c, h, w, k = map(int, input().split())
    knights[pid] = (r, c, h, w)
    knights_stamina[pid] = k
    for i in range(h):
        for j in range(w):
            knights_board[r + i][c + j] = pid
for _ in range(Q):
    pid, d = map(int, input().split())
    if not knights_stamina[pid]:
        continue
    knights_move(pid, d)
print(sum(damages))