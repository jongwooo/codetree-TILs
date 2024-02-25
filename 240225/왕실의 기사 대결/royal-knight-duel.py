def reach_the_wall(pid, dx, dy):
    global knight, board
    r, c, h, w, k = knight[pid]
    for i in range(h):
        for j in range(w):
            if board[r + i + dx][c + j + dy] == 2:
                return True
    return False


def knights_move(pid, dx, dy):
    stack = [pid]
    interaction_list = interaction(pid, dx, dy)
    while interaction_list:
        next_interaction = []
        for next_pid in interaction_list:
            if reach_the_wall(next_pid, dx, dy):
                return
            stack.append(next_pid)
            next_interaction += interaction(next_pid, dx, dy)
        interaction_list = next_interaction
    while stack:
        p = stack.pop()
        knight_move(p, dx, dy)
        if p != pid:
            check_trap(p)


def knight_move(pid, dx, dy):
    global knight, knight_board
    r, c, h, w, k = knight[pid]
    for i in range(h):
        for j in range(w):
            knight_board[r + i][c + j] = 0
    for i in range(h):
        for j in range(w):
            knight_board[r + i + dx][c + j + dy] = pid
    knight[pid] = (r + dx, c + dy, h, w, k)


def interaction(pid, dx, dy):
    global knight, knight_board
    r, c, h, w, k = knight[pid]
    interaction_list = set()
    for i in range(h):
        for j in range(w):
            if knight_board[r + i + dx][c + j + dy] != pid and knight_board[r + i + dx][c + j + dy] != 0:
                interaction_list.add(knight_board[r + i + dx][c + j + dy])
    return interaction_list


def check_trap(pid):
    global knight, board, damages
    r, c, h, w, k = knight[pid]
    for i in range(h):
        for j in range(w):
            if board[r + i][c + j] == 1:
                damages[pid] += 1
                k -= 1
                if k == 0:
                    break
        if k == 0:
            break
    if k == 0:
        delete_knight_from_board(pid)
    else:
        knight[pid] = (r, c, h, w, k)


def delete_knight_from_board(pid):
    global knight, knight_board
    r, c, h, w, k = knight[pid]
    game_over[pid] = True
    damages[pid] = 0
    del knight[pid]
    for i in range(h):
        for j in range(w):
            knight_board[r + i][c + j] = 0


L, N, Q = map(int, input().split())
board = [[2] * (L + 2)] + [[2] + list(map(int, input().split())) + [2] for _ in range(L)] + [[2] * (L + 2)]
knight = {}
knight_board = [[0] * (L + 2) for _ in range(L + 2)]
for pid in range(1, N + 1):
    r, c, h, w, k = map(int, input().split())
    for i in range(h):
        for j in range(w):
            knight_board[r + i][c + j] = pid
    knight[pid] = (r, c, h, w, k)
direction = ((-1, 0), (0, 1), (1, 0), (0, -1))
game_over = [False] * (N + 1)
damages = [0] * (N + 1)
for _ in range(Q):
    pid, d = map(int, input().split())
    dx, dy = direction[d]
    if game_over[pid]:
        continue
    if reach_the_wall(pid, dx, dy):
        continue
    knights_move(pid, dx, dy)
print(sum(damages))