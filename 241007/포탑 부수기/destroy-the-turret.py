from collections import deque


def find_attacker():
    candidates = []
    for i in range(N):
        for j in range(M):
            if turrets[i][j]:
                candidates.append((i, j, turrets[i][j], attack_history[i][j], i + j, i))
    candidates.sort(key=lambda c: (c[2], -c[3], -c[4], -c[5]))
    return candidates[0][0], candidates[0][1]


def find_target():
    candidates = []
    for i in range(N):
        for j in range(M):
            if turrets[i][j] and (i, j) is not (ax, ay):
                candidates.append((i, j, turrets[i][j], attack_history[i][j], i + j, i))
    candidates.sort(key=lambda c: (-c[2], c[3], c[4], c[5]))
    return candidates[0][0], candidates[0][1]


def laser_attack():
    queue = deque([(ax, ay, [])])
    visited = [[0] * M for _ in range(N)]
    visited[ax][ay] = 1
    while queue:
        x, y, laser_path = queue.popleft()
        if (x, y) == (tx, ty):
            return True, laser_path
        for dx, dy in laser_dirs:
            nx = x + dx
            ny = y + dy
            if 0 <= nx < N and 0 <= ny < M and not visited[nx][ny] and turrets[nx][ny]:
                queue.append((nx, ny, laser_path + [(nx, ny)]))
                visited[nx][ny] = 1
    return False, []


def cannon_attack():
    global turrets
    cannon_path = []
    for dx, dy in cannon_dirs:
        nx = (tx + dx) % N
        ny = (ty + dy) % M
        if turrets[nx][ny]:
            cannon_path.append((nx, ny))
    return cannon_path


def attack(atk_path):
    global turrets
    atk = turrets[ax][ay]
    for x, y in atk_path:
        if (x, y) == (tx, ty):
            turrets[x][y] -= atk
        else:
            turrets[x][y] -= atk // 2
        if turrets[x][y] < 0:
            turrets[x][y] = 0


def repair():
    global turrets
    for i in range(N):
        for j in range(M):
            if turrets[i][j] and (i, j) not in ((ax, ay), (tx, ty)):
                turrets[i][j] += 1


def only_one_turret_left():
    cnt = 0
    for i in range(N):
        for j in range(M):
            if turrets[i][j]:
                cnt += 1
    return cnt == 1


def find_max_atk_turret():
    max_atk = 0
    for i in range(N):
        for j in range(M):
            if turrets[i][j]:
                if max_atk < turrets[i][j]:
                    max_atk = turrets[i][j]
    return max_atk


N, M, K = map(int, input().split())
turrets = [list(map(int, input().split())) for _ in range(N)]
attack_history = [[0] * M for _ in range(N)]
laser_dirs = ((0, 1), (1, 0), (0, -1), (-1, 0))
cannon_dirs = ((0, 0), (0, 1), (0, -1), (1, 1), (1, -1), (1, 0), (-1, 1), (-1, -1), (-1, 0))
for turn in range(K):
    ax, ay = find_attacker()
    attack_history[ax][ay] = turn + 1
    turrets[ax][ay] += (N + M)
    tx, ty = find_target()
    success, path = laser_attack()
    if not success:
        path = cannon_attack()
    attack(path)
    repair()
    if only_one_turret_left():
        break
print(find_max_atk_turret())