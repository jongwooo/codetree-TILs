def initialize():
    global monsters
    x, y = n // 2, n // 2
    idx = 0
    dist = 1
    direction = 0
    move = 0
    while True:
        for _ in range(dist):
            monsters[idx] = grid[x][y]
            pos2idx[(x, y)] = idx
            nx = x + maze_dirs[direction][0]
            ny = y + maze_dirs[direction][1]
            if (nx, ny) == (0, -1):
                return
            idx += 1
            x, y = nx, ny
        move += 1
        direction = (direction + 1) % 4
        if move == 2:
            dist += 1
            move = 0


def attack(d, p):
    global monsters, score
    x, y = n // 2, n // 2
    dx, dy = attack_dirs[d]
    for i in range(1, p + 1):
        nx = x + dx * i
        ny = y + dy * i
        score += monsters[pos2idx[(nx, ny)]]
        monsters[pos2idx[(nx, ny)]] = -1


def remove_repeated_monsters():
    global score
    flag = False
    target = 0
    cnt = 0
    for i in range(n ** 2):
        if monsters[i] == monsters[target]:
            cnt += 1
        else:
            if 4 <= cnt:
                flag = True
                score += monsters[target] * cnt
                for j in range(target, i):
                    monsters[j] = -1
            target = i
            cnt = 1
    return flag


def tide_up():
    global monsters
    removed_cnt = monsters.count(-1)
    monsters = [monster for monster in monsters if monster != -1] + [0] * removed_cnt


def pair_monster_nums():
    global monsters
    new_monsters = [0]
    group = []
    for i in range(1, n ** 2):
        if not group:
            group.append(monsters[i])
        elif monsters[i] == group[0]:
            group.append(monsters[i])
        else:
            new_monsters.append(len(group))
            new_monsters.append(group[0])
            group = [monsters[i]]
    monsters = [0] * (n ** 2)
    for i in range(len(new_monsters)):
        if i >= (n ** 2):
            break
        monsters[i] = new_monsters[i]


n, m = map(int, input().split())
grid = [list(map(int, input().split())) for _ in range(n)]
monsters = [-1] * (n ** 2)
pos2idx = {}
attack_dirs = ((0, 1), (1, 0), (0, -1), (-1, 0))  # → ↓ ← ↑
maze_dirs = ((0, -1), (1, 0), (0, 1), (-1, 0))
initialize()
score = 0
for _ in range(m):
    d, p = map(int, input().split())
    attack(d, p)
    tide_up()
    while True:
        if not remove_repeated_monsters():
            break
        tide_up()
    pair_monster_nums()
print(score)