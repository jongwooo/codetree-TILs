from copy import deepcopy

EMPTY = 0


def int_minus_one():
    return lambda x: int(x) - 1


def distance_from_maze_exit(x, y):
    return abs(x - maze_exit[0]) + abs(y - maze_exit[1])


def in_range(x, y):
    return 0 <= x < N and 0 <= y < N


def players_move():
    global players, dist_sum
    for pid, player in enumerate(players):
        x, y = player
        cur_dist = distance_from_maze_exit(x, y)
        for dx, dy in dirs:
            nx = x + dx
            ny = y + dy
            new_dist = distance_from_maze_exit(nx, ny)
            if in_range(nx, ny) and maze[nx][ny] == EMPTY and new_dist < cur_dist:
                players[pid] = (nx, ny)
                dist_sum += 1
                break


def find_smallest_square():
    candidates = []
    ex, ey = maze_exit
    for x, y in players:
        row = abs(x - ex)
        col = abs(y - ey)
        d = max(row, col)
        r = min(x, ex)
        c = min(y, ey)
        if row < col:
            r = max(x, ex) - d
            if r < 0:
                r = 0
        elif col < row:
            c = max(y, ey) - d
            if c < 0:
                c = 0
        candidates.append((d, r, c))
    candidates.sort()
    return candidates[0]


def rotate(d, r, c):
    global maze, players, maze_exit
    temp_maze = deepcopy(maze)
    temp_players = []
    temp_exit = maze_exit
    for i in range(d + 1):
        for j in range(d + 1):
            if temp_maze[r + i][c + j] > 0:
                temp_maze[r + i][c + j] -= 1
            maze[r + j][c + d - i] = temp_maze[r + i][c + j]
            cur = (r + i, c + j)
            rotated = (r + j, c + d - i)
            while cur in players:
                players.remove(cur)
                temp_players.append(rotated)
            if cur == maze_exit:
                temp_exit = rotated
    players += temp_players
    maze_exit = temp_exit


dirs = ((-1, 0), (1, 0), (0, -1), (0, 1))
N, M, K = map(int, input().split())
maze = [list(map(int, input().split())) for _ in range(N)]
players = [tuple(map(int_minus_one(), input().split())) for _ in range(M)]
dist_sum = 0
maze_exit = tuple(map(int_minus_one(), input().split()))
for _ in range(K):
    players_move()
    while maze_exit in players:
        players.remove(maze_exit)
    if not players:
        break
    d, r, c = find_smallest_square()
    rotate(d, r, c)
print(dist_sum)
print(maze_exit[0] + 1, maze_exit[1] + 1)