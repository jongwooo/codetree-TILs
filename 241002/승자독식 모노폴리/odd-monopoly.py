def int_minus_one():
    return lambda x: int(x) - 1


def initialize():
    global exclusive_contracts, player_pos
    for i in range(n):
        for j in range(n):
            if grid[i][j]:
                exclusive_contracts[i][j] = (k, grid[i][j])
                player_pos[grid[i][j]] = (i, j)


def players_move():
    temp = [[[] for _ in range(n)] for _ in range(n)]
    for pid in range(1, m + 1):
        if not alive[pid]:
            continue
        x, y = player_pos[pid]
        cur_d = player_d[pid - 1]
        player_d_priority = player_d_priorities[4 * (pid - 1) + cur_d]
        moved = False
        for d in player_d_priority:
            dx, dy = dirs[d]
            nx = x + dx
            ny = y + dy
            if 0 <= nx < n and 0 <= ny < n and exclusive_contracts[nx][ny] == (0, 0):
                temp[nx][ny].append(pid)
                player_pos[pid] = (nx, ny)
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
                player_pos[pid] = (nx, ny)
                player_d[pid - 1] = d
                moved = True
                break
        if moved:
            continue
        temp[x][y].append(pid)
    for i in range(n):
        for j in range(n):
            if not temp[i][j]:
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
                    delete_player(temp_id)


def delete_player(pid):
    global player_pos, alive
    del player_pos[pid]
    alive[pid] = 0


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


def check_only_1st_player_alive():
    return sum(alive) == 1 and alive[1]


dirs = ((-1, 0), (1, 0), (0, -1), (0, 1))
n, m, k = map(int, input().split())
grid = [list(map(int, input().split())) for _ in range(n)]
exclusive_contracts = [[(0, 0) for _ in range(n)] for _ in range(n)]  # (time, pid)
player_pos = dict()
player_d = list(map(int_minus_one(), input().split()))
player_d_priorities = [tuple(map(int_minus_one(), input().split())) for _ in range(m * 4)]
alive = [0] + [1] * m
initialize()
turn_cnt = 1
for _ in range(1_000):
    players_move()
    if check_only_1st_player_alive():
        break
    decrease_time()
    turn_cnt += 1
print(turn_cnt if turn_cnt < 1_000 else -1)