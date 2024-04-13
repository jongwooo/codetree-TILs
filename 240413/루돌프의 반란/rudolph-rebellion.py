def in_board(x, y):
    return 0 <= x < N and 0 <= y < N


def distance_from_rudolph(r, c):
    return (rx - r) ** 2 + (ry - c) ** 2


def find_nearest_santa_loc():
    santa_candidates = []
    for sid in range(P):
        if game_over[sid]:
            continue
        sx, sy = santa_loc[sid]
        santa_candidates.append((distance_from_rudolph(sx, sy), sx, sy))
    santa_candidates.sort(key=lambda x: (x[0], -x[1], -x[2]))
    return santa_candidates[0][1:]


def check_direction(x, y):
    dx, dy = 0, 0
    if rx > x:
        dx -= 1
    elif rx < x:
        dx += 1
    if ry > y:
        dy -= 1
    elif ry < y:
        dy += 1
    return dx, dy


def rudolph_move(k):
    global board, rx, ry
    sx, sy = find_nearest_santa_loc()
    dx, dy = check_direction(sx, sy)
    nx = rx + dx
    ny = ry + dy
    if board[nx][ny] >= 0:  # 산타가 있을 경우 충돌
        crash_rudolph_to_santa(board[nx][ny], dx, dy, k)
    board[rx][ry] = -1
    board[nx][ny] = -2
    rx, ry = nx, ny


def crash_rudolph_to_santa(sid, dx, dy, k):
    global board, scores, game_over, alive
    sx, sy = santa_loc[sid]
    panic[sid] = k + 1
    scores[sid] += C
    nx = sx + dx * C
    ny = sy + dy * C
    if not in_board(nx, ny):
        game_over[sid] = True
        board[sx][sy] = -1
        alive -= 1
        return
    if board[nx][ny] >= 0:  # 만약 해당 칸에 다른 산타가 있으면
        interaction(nx, ny, dx, dy)  # 상호작용
    board[sx][sy] = -1
    board[nx][ny] = sid
    santa_loc[sid] = (nx, ny)


def santa_move(k):
    for sid in range(P):  # 각 산타마다
        if panic[sid] >= k or game_over[sid]:  # 기절했거나 탈락했다면
            continue  # 건너뛴다
        sx, sy = santa_loc[sid]
        possible_loc = []
        cur_dist = distance_from_rudolph(sx, sy)
        for d in range(4):
            dx, dy = santa_dirs[d]
            nx = sx + dx
            ny = sy + dy
            if in_board(nx, ny) and board[nx][ny] < 0:
                dist = distance_from_rudolph(nx, ny)
                if dist < cur_dist:
                    possible_loc.append((dist, d, nx, ny))
        if not possible_loc:
            continue
        possible_loc.sort()
        d, nx, ny = possible_loc[0][1:]
        board[sx][sy] = -1
        if board[nx][ny] == -2:
            dx, dy = santa_dirs[d]
            crash_santa_to_rudolph(sid, dx, dy, k)
        else:
            board[nx][ny] = sid
            santa_loc[sid] = (nx, ny)


def crash_santa_to_rudolph(sid, dx, dy, k):
    global board, scores, game_over, alive
    sx, sy = santa_loc[sid]
    panic[sid] = k + 1
    scores[sid] += D
    nx = rx - dx * D
    ny = ry - dy * D
    if not in_board(nx, ny):
        game_over[sid] = True
        board[sx][sy] = -1
        alive -= 1
        return
    if board[nx][ny] >= 0:  # 만약 해당 칸에 다른 산타가 있으면
        interaction(nx, ny, -dx, -dy)  # 상호작용
    board[sx][sy] = -1
    board[nx][ny] = sid
    santa_loc[sid] = (nx, ny)


def interaction(x, y, dx, dy):
    global board, game_over, alive
    sid = board[x][y]
    nx = x + dx
    ny = y + dy
    if not in_board(nx, ny):
        game_over[sid] = True
        alive -= 1
        return
    if board[nx][ny] >= 0:  # 만약 해당 칸에 다른 산타가 있으면
        interaction(nx, ny, dx, dy)  # 상호작용
    board[nx][ny] = sid
    santa_loc[sid] = (nx, ny)


def plus_one_point_for_alive_santa():
    global scores
    for sid in range(P):
        if not game_over[sid]:
            scores[sid] += 1


N, M, P, C, D = map(int, input().split())
board = [[-1] * N for _ in range(N)]  # 빈 공간 (-1)
rx, ry = map(lambda x: int(x) - 1, input().split())
board[rx][ry] = -2  # 루돌프 위치 표시 (-2)
santa_loc = [tuple() for _ in range(P)]
for _ in range(P):
    sid, sx, sy = map(lambda x: int(x) - 1, input().split())
    board[sx][sy] = sid  # 산타 위치 표시 (sid)
    santa_loc[sid] = (sx, sy)  # 산타 위치 정보 등록
santa_dirs = ((-1, 0), (0, 1), (1, 0), (0, -1))  # 상 우 하 좌
panic = [0] * P
alive = P
game_over = [False] * P
scores = [0] * P
for k in range(1, M + 1):
    rudolph_move(k)
    santa_move(k)
    if alive <= 0:
        break
    plus_one_point_for_alive_santa()
print(*scores)