EMPTY = 0
TRAP = 1
WALL = 2


def reach_the_wall(pid, d):
    global knight, board
    r, c, h, w, k = knight[pid]
    dr, dc = dirs[d]
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
            if reach_the_wall(next_pid, d):  # 기사가 이동하려는 방향의 끝에 벽이 있다면 모든 기사는 이동할 수 없게 된다.
                return
            if next_pid in stack:
                stack.remove(next_pid)
            stack.append(next_pid)
            next_interaction_set.update(interaction(next_pid, d))
        interaction_set = next_interaction_set
    while stack:
        p = stack.pop()
        knight_move(p, d)
        if p != pid:
            check_trap(p)


def knight_move(pid, d):
    global knight, knight_board
    r, c, h, w, k = knight[pid]
    dr, dc = dirs[d]
    for i in range(h):
        for j in range(w):
            knight_board[r + i][c + j] = EMPTY
    for i in range(h):
        for j in range(w):
            knight_board[r + i + dr][c + j + dc] = pid
    knight[pid] = (r + dr, c + dc, h, w, k)  # 위치 정보 업데이트


def interaction(pid, d):
    global knight, knight_board
    r, c, h, w, k = knight[pid]
    dr, dc = dirs[d]
    interaction_set = set()
    for i in range(h):
        for j in range(w):
            if knight_board[r + i + dr][c + j + dc] != pid and knight_board[r + i + dr][c + j + dc] != EMPTY:
                interaction_set.add(knight_board[r + i + dr][c + j + dc])
    return interaction_set


def check_trap(pid):
    global knight, board, damages
    r, c, h, w, k = knight[pid]
    for i in range(h):
        for j in range(w):
            if board[r + i][c + j] == TRAP:
                damages[pid] += 1
                k -= 1
            if k == 0:
                delete_knight_from_board(pid)
                return
    knight[pid] = (r, c, h, w, k)


def delete_knight_from_board(pid):
    global knight, knight_board
    r, c, h, w, k = knight[pid]
    game_over[pid] = True
    damages[pid] = 0
    del knight[pid]
    for i in range(h):
        for j in range(w):
            knight_board[r + i][c + j] = EMPTY


L, N, Q = map(int, input().split())
board = [[WALL] * (L + 2)] + [[WALL] + list(map(int, input().split())) + [WALL] for _ in range(L)] + [
    [WALL] * (L + 2)]  # 빈칸, 함정, 벽 정보
knight = dict()  # 기사 정보 (r, c, h, w, k)
knight_board = [[EMPTY] * (L + 2) for _ in range(L + 2)]  # 기사 위치 정보 (pid)
for pid in range(1, N + 1):
    r, c, h, w, k = map(int, input().split())
    knight[pid] = (r, c, h, w, k)
    for i in range(h):
        for j in range(w):
            knight_board[r + i][c + j] = pid
dirs = ((-1, 0), (0, 1), (1, 0), (0, -1))  # 위쪽, 오른쪽, 아래쪽, 왼쪽
game_over = [False] * (N + 1)
damages = [0] * (N + 1)
for _ in range(Q):
    pid, d = map(int, input().split())
    if game_over[pid]:  # 체스판에서 사라진 기사에게 명령을 내리면 아무런 반응이 없게 된다.
        continue
    if reach_the_wall(pid, d):  # 기사가 이동하려는 방향의 끝에 벽이 있다면 이동할 수 없다.
        continue
    knights_move(pid, d)
print(sum(damages))