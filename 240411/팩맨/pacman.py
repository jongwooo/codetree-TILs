import copy
import sys


def spawn_monster_eggs():
    global eggs
    eggs = copy.deepcopy(monsters)


def monsters_move():
    global monsters
    moved = [[[] for _ in range(4)] for _ in range(4)]
    for x in range(4):
        for y in range(4):
            while monsters[x][y]:
                md = monsters[x][y].pop()
                for _ in range(8):
                    dx, dy = monster_dirs[md]
                    nx = x + dx
                    ny = y + dy
                    if 0 <= nx < 4 and 0 <= ny < 4 and not corpses[nx][ny] and (nx, ny) != (px, py):
                        moved[nx][ny].append(md)
                        break
                    md = (md + 1) % 8  # 가능할 때까지 반시계 방향으로 45도씩 회전
                else:
                    moved[x][y].append(md)
    monsters = moved


def packman_move():
    global monsters, eaten, max_eat
    max_eat = -1
    dfs(px, py, 0, 0, [])
    for x, y in eaten:
        if monsters[x][y]:
            monsters[x][y] = []  # 팩맨이 해당 위치의 몬스터를 먹는다
            corpses[x][y] = 3


def dfs(x, y, depth, eat_cnt, visited):
    global px, py, eaten, max_eat
    if depth == 3:
        if max_eat < eat_cnt:
            max_eat = eat_cnt
            px, py = x, y  # 경로의 최종 위치로 이동
            eaten = visited[:]  # 가장 많이 먹었을 때의 경로
        return
    for dx, dy in packman_dirs:
        nx = x + dx
        ny = y + dy
        if 0 <= nx < 4 and 0 <= ny < 4:
            if (nx, ny) not in visited:
                visited.append((nx, ny))
                dfs(nx, ny, depth + 1, eat_cnt + len(monsters[nx][ny]), visited)
                visited.pop()
            else:
                dfs(nx, ny, depth + 1, eat_cnt, visited)


def destroy_monster_corpses():
    for x in range(4):
        for y in range(4):
            if corpses[x][y]:
                corpses[x][y] -= 1


def hatch_monster_eggs():
    global monsters
    for x in range(4):
        for y in range(4):
            monsters[x][y] += eggs[x][y]


m, t = map(int, sys.stdin.readline().split())
px, py = map(lambda x: int(x) - 1, sys.stdin.readline().split())  # 1만큼 보정
monsters = [[[] for _ in range(4)] for _ in range(4)]  # 몬스터 위치 정보
corpses = [[0] * 4 for _ in range(4)]  # 몬스터 시체 정보
eggs = []  # 부화할 알 위치 정보
eaten = []
max_eat = -1
monster_dirs = ((-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1))  # ↑, ↖, ←, ↙, ↓, ↘, →, ↗
packman_dirs = ((-1, 0), (0, -1), (1, 0), (0, 1))  # 상-좌-하-우의 우선순위
for _ in range(m):
    r, c, d = map(int, sys.stdin.readline().split())
    monsters[r - 1][c - 1].append(d - 1)
for _ in range(t):
    spawn_monster_eggs()  # 몬스터 복제 시도
    monsters_move()  # 몬스터 이동
    packman_move()  # 팩맨 이동
    destroy_monster_corpses()  # 몬스터 시체 소멸
    hatch_monster_eggs()  # 몬스터 복제 완성
alive = 0
for i in range(4):
    for j in range(4):
        alive += len(monsters[i][j])
print(alive)