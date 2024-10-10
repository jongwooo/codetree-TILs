from copy import deepcopy


def int_minus_one():
    return lambda k: int(k) - 1


def in_range(r, c):
    return 0 <= r < 4 and 0 <= c < 4


def spawn_monster_eggs():
    global eggs
    eggs = deepcopy(monsters)


def monsters_move():
    global monsters
    temp = [[[] for _ in range(4)] for _ in range(4)]
    for r in range(4):
        for c in range(4):
            if not monsters[r][c]:
                continue
            while monsters[r][c]:
                d = monsters[r][c].pop()
                for _ in range(8):
                    dr, dc = monster_dirs[d]
                    nr = r + dr
                    nc = c + dc
                    if in_range(nr, nc) and not corpses[nr][nc] and (nr, nc) != (pr, pc):
                        temp[nr][nc].append(d)
                        break
                    d = (d + 1) % 8
                else:
                    temp[r][c].append(d)
    monsters = temp


def pacman_move():
    global monsters, eaten, max_eat, corpses
    max_eat = -1
    dfs(pr, pc, 0, 0, [])
    for r, c in eaten:
        if monsters[r][c]:
            monsters[r][c].clear()
            corpses[r][c] = 3


def dfs(r, c, depth, eat_cnt, visited):
    global pr, pc, eaten, max_eat
    if depth == 3:
        if max_eat < eat_cnt:
            max_eat = eat_cnt
            pr, pc = r, c
            eaten = visited[:]
        return 
    for dr, dc in pacman_dirs:
        nr = r + dr
        nc = c + dc
        if in_range(nr, nc):
            if (nr, nc) not in visited:
                visited.append((nr, nc))
                dfs(nr, nc, depth + 1, eat_cnt + len(monsters[nr][nc]), visited)
                visited.pop()
            else:
                dfs(nr, nc, depth + 1, eat_cnt, visited)


def destroy_monster_corpses():
    global corpses
    for r in range(4):
        for c in range(4):
            if corpses[r][c]:
                corpses[r][c] -= 1


def hatch_monster_eggs():
    global monsters
    for r in range(4):
        for c in range(4):
            monsters[r][c] += eggs[r][c]


monster_dirs = ((-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1))  # ↑, ↖, ←, ↙, ↓, ↘, →, ↗
pacman_dirs = ((-1, 0), (0, -1), (1, 0), (0, 1))  # 상 좌 하 우
m, t = map(int, input().split())
pr, pc = map(int_minus_one(), input().split())
monsters = [[[] for _ in range(4)] for _ in range(4)]
eggs = []
corpses = [[0] * 4 for _ in range(4)]
eaten = []
max_eat = -1
for mid in range(m):
    r, c, d = map(int_minus_one(), input().split())
    monsters[r][c].append(d)
for _ in range(t):
    spawn_monster_eggs()
    monsters_move()
    pacman_move()
    destroy_monster_corpses()
    hatch_monster_eggs()
alive = 0
for r in range(4):
    for c in range(4):
        alive += len(monsters[r][c])
print(alive)