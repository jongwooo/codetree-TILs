import sys


def spawn_monster_eggs():
    global eggs, eggs_d
    eggs = monsters[:]  # 몬스터 위치 정보 복제
    eggs_d = monsters_d[:]  # 몬스터 방향 정보 복제


def monsters_move():
    for mid in range(len(monsters)):
        mx, my = monsters[mid]
        md = monsters_d[mid]
        for _ in range(8):
            dx, dy = monster_dirs[md]
            nx = mx + dx
            ny = my + dy
            if 0 <= nx < 4 and 0 <= ny < 4 and (nx, ny) not in monster_corpses and (nx, ny) != (px, py):
                monsters[mid] = (nx, ny)
                monsters_d[mid] = md
                break
            md = (md + 1) % 8  # 가능할 때까지 반시계 방향으로 45도씩 회전


def packman_move():
    global monsters, monsters_d, alive, eaten
    dfs(px, py, 0, [], [])
    alive -= len(eaten)
    eaten.sort(reverse=True)
    for mid in eaten:  # 팩맨이 먹은 몬스터 리스트를 거꾸로 순회하며 시체 정보 추가 / 몬스터 정보 삭제
        monster_corpses.append(monsters[mid])
        monster_corpse_lifetimes.append(2)
        del monsters[mid]
        del monsters_d[mid]


def dfs(x, y, depth, eaten_scheduled, visited):
    global px, py, max_eat, eaten
    if depth == 3:
        if max_eat < len(eaten_scheduled):
            max_eat = len(eaten_scheduled)
            px, py = x, y
            eaten = eaten_scheduled
        return
    for dx, dy in packman_dirs:
        nx = x + dx
        ny = y + dy
        if 0 <= nx < 4 and 0 <= ny < 4:
            if (nx, ny) not in visited:
                visited.append((nx, ny))
                temp = []
                for mid, monster in enumerate(monsters):
                    if (nx, ny) == monster:
                        temp.append(mid)
                dfs(nx, ny, depth + 1, eaten_scheduled + temp, visited)
                visited.pop()
            else:
                dfs(nx, ny, depth + 1, eaten_scheduled, visited)


def destroy_monster_corpses():
    global monster_corpses, monster_corpse_lifetimes
    destroy_scheduled = []  # 몬스터 시체 소멸 예정 id
    for cid in range(len(monster_corpses)):
        monster_corpse_lifetimes[cid] -= 1
        if monster_corpse_lifetimes[cid] == 0:
            destroy_scheduled.append(cid)  # 2턴이 지나면 소멸 예정 리스트에 추가
    for cid in destroy_scheduled[::-1]:  # 소멸 예정 리스트를 거꾸로 순회하며 시체 정보 삭제
        del monster_corpses[cid]
        del monster_corpse_lifetimes[cid]


def hatch_monster_eggs():
    global monsters, monsters_d, alive, eggs, eggs_d
    monsters += eggs
    monsters_d += eggs_d
    alive += len(eggs)  # 부화한 만큼 살아 남은 몬스터 마리 수 추가
    eggs = []  # 부화 이후 알 위치 정보 초기화
    eggs_d = []  # 부화 이후 알 방향 정보 초기화


m, t = map(int, sys.stdin.readline().split())
px, py = map(lambda x: int(x) - 1, sys.stdin.readline().split())  # 1만큼 보정
monsters = []  # 몬스터 위치 정보
monsters_d = []  # 몬스터 방향 정보
monster_corpses = []  # 몬스터 시체 정보
monster_corpse_lifetimes = []  # 몬스터 시체 소멸 대기 시간 (총 2턴 동안 시체 유지)
eggs = []  # 부화 전의 알 위치 정보
eggs_d = []  # 알 방향 정보
eaten = []
monster_dirs = ((-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1))  # ↑, ↖, ←, ↙, ↓, ↘, →, ↗
packman_dirs = ((-1, 0), (0, -1), (1, 0), (0, 1))  # 상-좌-하-우의 우선순위
for _ in range(m):
    r, c, d = map(int, sys.stdin.readline().split())
    monsters.append((r - 1, c - 1))  # 몬스터의 위치 정보 저장, 1만큼 보정
    monsters_d.append(d - 1)  # d는 1부터 시작하므로 1만큼 보정
alive = m  # 초기의 살아 남은 몬스터 수 정보 m
for _ in range(t):
    max_eat = -1
    spawn_monster_eggs()  # 몬스터 복제 시도
    monsters_move()  # 몬스터 이동
    packman_move()  # 팩맨 이동
    destroy_monster_corpses()  # 몬스터 시체 소멸
    hatch_monster_eggs()  # 몬스터 복제 완성
print(alive)