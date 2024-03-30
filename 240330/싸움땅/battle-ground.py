import sys


def in_range(nx, ny):
    return 0 <= nx < n and 0 <= ny < n


def find_move_loc(pid):
    x, y, d, _, _ = player_info[pid]
    nx = x + dx[d]
    ny = y + dy[d]
    if not in_range(nx, ny):
        turn_back_d = (d + 2) % 4
        player_info[pid][2] = turn_back_d
        nx = x + dx[turn_back_d]
        ny = y + dy[turn_back_d]
    return nx, ny


def move(pid, nx, ny):
    x, y = player_info[pid][0], player_info[pid][1]
    players[x][y] = -1
    player_info[pid][0], player_info[pid][1] = nx, ny
    players[nx][ny] = pid


def pick_up_the_gun(pid, nx, ny):
    guns[nx][ny].sort()
    if player_info[pid][4] == 0:
        player_info[pid][4] = guns[nx][ny][-1]
        guns[nx][ny].pop()
    else:
        player_gun = player_info[pid][4]
        atk_max_gun = guns[nx][ny][-1]
        if player_gun >= atk_max_gun:
            return
        player_info[pid][4], guns[nx][ny][-1] = guns[nx][ny][-1], player_info[pid][4]


def fight(pid1, pid2):
    pid1_stat, pid1_gun = player_info[pid1][3], player_info[pid1][4]
    pid2_stat, pid2_gun = player_info[pid2][3], player_info[pid2][4]
    if pid1_stat + pid1_gun > pid2_stat + pid2_gun:
        return pid1, pid2, abs(pid1_stat + pid1_gun - pid2_stat - pid2_gun)
    elif pid1_stat + pid1_gun < pid2_stat + pid2_gun:
        return pid2, pid1, abs(pid1_stat + pid1_gun - pid2_stat - pid2_gun)
    elif pid1_stat > pid2_stat:
        return pid1, pid2, abs(pid1_stat + pid1_gun - pid2_stat - pid2_gun)
    else:
        return pid2, pid1, abs(pid1_stat + pid1_gun - pid2_stat - pid2_gun)


def drop_all_guns(pid, nx, ny):
    guns[nx][ny].append(player_info[pid][4])
    player_info[pid][4] = 0


def find_loser_loc(pid):
    x, y, d = player_info[pid][0], player_info[pid][1], player_info[pid][2]
    nx = x + dx[d]
    ny = y + dy[d]
    while not (in_range(nx, ny) and players[nx][ny] == -1):
        d = (d + 1) % 4
        player_info[pid][2] = d
        nx = x + dx[d]
        ny = y + dy[d]
    return nx, ny


n, m, k = map(int, sys.stdin.readline().split())
guns = [[[] for _ in range(n)] for _ in range(n)]
for i in range(n):
    gun_list = list(map(int, sys.stdin.readline().split()))
    for j in range(n):
        if gun_list[j] != 0:
            guns[i][j].append(gun_list[j])
players = [[-1] * n for _ in range(n)]
player_info = []
for pid in range(m):
    x, y, d, s = map(int, sys.stdin.readline().split())
    players[x - 1][y - 1] = pid
    player_info.append([x - 1, y - 1, d, s, 0])
scores = [0] * m
dx = (-1, 0, 1, 0)
dy = (0, 1, 0, -1)
for _ in range(k):
    for pid in range(m):
        nx, ny = find_move_loc(pid)
        if players[nx][ny] == -1:
            if len(guns[nx][ny]) == 0:
                move(pid, nx, ny)
                continue
            pick_up_the_gun(pid, nx, ny)
            move(pid, nx, ny)
        else:
            winner, loser, score = fight(pid, players[nx][ny])
            scores[winner] += score
            move(pid, nx, ny)
            drop_all_guns(loser, nx, ny)
            lx, ly = find_loser_loc(loser)
            move(loser, lx, ly)
            if len(guns[lx][ly]) != 0:
                pick_up_the_gun(loser, lx, ly)
            pick_up_the_gun(winner, nx, ny)
            players[nx][ny] = winner
print(*scores)