from collections import deque


def find_attacker():
    attacker_candidates = []
    for i in range(N):
        for j in range(M):
            if turrets[i][j] != 0:
                attacker_candidates.append((i, j, turrets[i][j], attack_history[i][j], i + j, j))
    attacker_candidates.sort(key=lambda x: (x[2], -x[3], -x[4], -x[5]))
    return attacker_candidates[0][0], attacker_candidates[0][1]


def find_target():
    global attacker
    target_candidates = []
    for i in range(N):
        for j in range(M):
            if turrets[i][j] != 0 and (i, j) != attacker:
                target_candidates.append((i, j, turrets[i][j], attack_history[i][j], i + j, j))
    target_candidates.sort(key=lambda x: (-x[2], x[3], x[4], x[5]))
    return target_candidates[0][0], target_candidates[0][1]


def find_lazer_path():
    global attacker, target
    queue = deque([(attacker[0], attacker[1], [])])
    visited = [[False] * M for _ in range(N)]
    visited[attacker[0]][attacker[1]] = True
    while queue:
        x, y, lazer_path = queue.popleft()
        if (x, y) == target:
            return True, lazer_path
        for dx, dy in lazer_dir:
            nx = (x + dx) % N
            ny = (y + dy) % M
            if turrets[nx][ny] != 0 and not visited[nx][ny]:
                new_path = lazer_path + [(nx, ny)]
                queue.append((nx, ny, new_path))
                visited[nx][ny] = True
    return False, lazer_path


def find_cannon_path():
    global attacker, target
    cannon_path = [target]
    for dx, dy in cannon_dir:
        nx = (target[0] + dx) % N
        ny = (target[1] + dy) % M
        if turrets[nx][ny] != 0 and (nx, ny) != attacker:
            cannon_path.append((nx, ny))
    return cannon_path


def attack(attack_path):
    global attacker, target
    atk = turrets[attacker[0]][attacker[1]]
    for x, y in attack_path:
        if (x, y) == target:
            turrets[x][y] -= atk
        else:
            turrets[x][y] -= atk // 2
        if turrets[x][y] < 0:
            turrets[x][y] = 0


def only_one_turret_left():
    cnt = 0
    for i in range(N):
        for j in range(M):
            if turrets[i][j] > 0:
                cnt += 1
    return cnt == 1


def repair():
    global attacker, path
    for i in range(N):
        for j in range(M):
            if turrets[i][j] != 0 and (i, j) != attacker and (i, j) not in path:
                turrets[i][j] += 1


N, M, K = map(int, input().split())
turrets = [list(map(int, input().split())) for _ in range(N)]
attack_history = [[0] * M for _ in range(N)]
lazer_dir = ((0, 1), (1, 0), (0, -1), (-1, 0))
cannon_dir = ((0, 1), (0, -1), (1, 1), (1, -1), (1, 0), (-1, 1), (-1, -1), (-1, 0))

for turn in range(K):
    attacker = find_attacker()
    attack_history[attacker[0]][attacker[1]] = turn + 1
    turrets[attacker[0]][attacker[1]] += N + M
    target = find_target()

    success, path = find_lazer_path()
    if not success:
        path = find_cannon_path()
    attack(path)

    if only_one_turret_left():
        break
    repair()

result = 0
for i in range(N):
    for j in range(M):
        if result < turrets[i][j]:
            result = turrets[i][j]
print(result)