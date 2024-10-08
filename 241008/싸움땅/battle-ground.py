EMPTY = 0


def in_range(x, y):
    return 0 <= x < n and 0 <= y < n


def turn():
    global player_pos, player_d
    for pid in range(m):
        x, y = player_pos[pid]
        d = player_d[pid]
        dx, dy = dirs[d]
        nx = x + dx
        ny = y + dy
        if not in_range(nx, ny):
            nx = x - dx
            ny = y - dy
            player_d[pid] = (d + 2) % 4
        if (nx, ny) not in player_pos:
            player_pos[pid] = (nx, ny)
            pick_up_strongest_gun(pid, nx, ny)
        else:
            pid2 = player_pos.index((nx, ny))
            player_pos[pid] = (nx, ny)
            fight_players = [(pid, player_stats[pid] + player_guns[pid], player_stats[pid]),
                             (pid2, player_stats[pid2] + player_guns[pid2], player_stats[pid2])]
            fight_players.sort(key=lambda f: (-f[1], -f[2]))
            win_player, _, _ = fight_players[0]
            points[win_player] += abs((player_stats[pid] + player_guns[pid]) - (player_stats[pid2] + player_guns[pid2]))
            lose_player, _, _ = fight_players[1]
            if player_guns[lose_player]:
                guns[nx][ny].append(player_guns[lose_player])
                player_guns[lose_player] = EMPTY
            d = player_d[lose_player]
            for _ in range(4):
                dx, dy = dirs[d]
                lx = nx + dx
                ly = ny + dy
                if in_range(lx, ly) and (lx, ly) not in player_pos:
                    player_pos[lose_player] = (lx, ly)
                    player_d[lose_player] = d
                    pick_up_strongest_gun(lose_player, lx, ly)
                    break
                d = (d + 1) % 4
            pick_up_strongest_gun(win_player, nx, ny)


def pick_up_strongest_gun(pid, x, y):
    if not guns[x][y]:
        return
    if player_guns[pid]:
        guns[x][y].append(player_guns[pid])
    strongest_gun = max(guns[x][y])
    guns[x][y].remove(strongest_gun)
    player_guns[pid] = strongest_gun


dirs = ((-1, 0), (0, 1), (1, 0), (0, -1))  # ↑, →, ↓, ←
n, m, k = map(int, input().split())
guns = [[[] for _ in range(n)] for _ in range(n)]
for i in range(n):
    temp = list(map(int, input().split()))
    for j in range(n):
        if temp[j]:
            guns[i][j].append(temp[j])
player_pos = []
player_d = [0] * m
player_stats = [0] * m
player_guns = [0] * m
for pid in range(m):
    x, y, player_d[pid], player_stats[pid] = map(int, input().split())
    player_pos.append((x - 1, y - 1))
points = [0] * m
for _ in range(k):
    turn()
print(*points)