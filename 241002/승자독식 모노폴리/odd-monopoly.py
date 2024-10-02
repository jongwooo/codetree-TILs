def int_minus_one():
    return lambda x: int(x) - 1


def players_contract():
    global exclusive_contracts
    for i in range(n):
        for j in range(n):
            if grid[i][j]:
                exclusive_contracts[i][j] = (k, grid[i][j])


def players_move():
    global grid, exclusive_contracts, player_d
    temp = [[[] for _ in range(n)] for _ in range(n)]
    for x in range(n):
        for y in range(n):
            if grid[x][y]:
                pid = grid[x][y]
                cur_d = player_d[pid - 1]
                player_d_priority = player_d_priorities[4 * (pid - 1) + cur_d]
                moved = False
                for d in player_d_priority:
                    dx, dy = dirs[d]
                    nx = x + dx
                    ny = y + dy
                    if 0 <= nx < n and 0 <= ny < n and exclusive_contracts[nx][ny] == (0, 0):
                        temp[nx][ny].append(pid)
                        player_d[pid - 1] = d
                        moved = True
                        break
                if moved:
                    continue
                for d in player_d_priority:
                    dx, dy = dirs[d]
                    nx = x + dx
                    ny = y + dy
                    if 0 <= nx < n and 0 <= ny < n and exclusive_contracts[nx][ny][1] == pid:
                        temp[nx][ny].append(pid)
                        player_d[pid - 1] = d
                        break
    for i in range(n):
        for j in range(n):
            if not temp[i][j]:
                grid[i][j] = 0
                continue
            if len(temp[i][j]) == 1:
                exclusive_contracts[i][j] = (k, temp[i][j][0])
                grid[i][j] = temp[i][j][0]
                continue
            min_player = min(temp[i][j])
            exclusive_contracts[i][j] = (k, min_player)
            grid[i][j] = min_player
            for temp_id in temp[i][j]:
                if temp_id != min_player:
                    alive[temp_id] = 0


def decrease_time():
    global exclusive_contracts
    for i in range(n):
        for j in range(n):
            if exclusive_contracts[i][j] == (0, 0):
                continue
            time, pid = exclusive_contracts[i][j]
            time -= 1
            if time == 0:
                exclusive_contracts[i][j] = (0, 0)
            else:
                exclusive_contracts[i][j] = (time, pid)


def check_only_one_player_alive():
    return sum(alive) == 1


dirs = ((-1, 0), (1, 0), (0, -1), (0, 1))
n, m, k = map(int, input().split())
grid = [list(map(int, input().split())) for _ in range(n)]
exclusive_contracts = [[(0, 0) for _ in range(n)] for _ in range(n)]  # (time, pid)
player_d = list(map(int_minus_one(), input().split()))
player_d_priorities = [tuple(map(int_minus_one(), input().split())) for _ in range(m * 4)]
alive = [0] + [1] * m
turn_cnt = 1
for _ in range(1_000):
    players_contract()
    players_move()
    decrease_time()
    if check_only_one_player_alive():
        break
    turn_cnt += 1
print(turn_cnt if turn_cnt < 1_000 else -1)