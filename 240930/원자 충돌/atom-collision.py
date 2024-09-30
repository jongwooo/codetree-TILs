def atoms_move():
    global grid
    temp = [[[] for _ in range(N)] for _ in range(N)]
    for x in range(N):
        for y in range(N):
            while grid[x][y]:
                m, s, d = grid[x][y].pop()
                nx = (x + dirs[d][0] * s) % N
                ny = (y + dirs[d][1] * s) % N
                temp[nx][ny].append((m, s, d))
    grid = temp


def atoms_synthesis():
    global grid
    temp = [[[] for _ in range(N)] for _ in range(N)]
    for x in range(N):
        for y in range(N):
            if 2 <= len(grid[x][y]):
                atom_cnt = len(grid[x][y])
                m_sum, s_sum = 0, 0
                udlr, diagonal = 0, 0
                while grid[x][y]:
                    m, s, d = grid[x][y].pop()
                    m_sum += m
                    s_sum += s
                    if d % 2 == 0:
                        udlr += 1
                    else:
                        diagonal += 1
                synthesis_m = m_sum // 5
                synthesis_s = s_sum // atom_cnt
                synthesis_d = 0
                if synthesis_m == 0:
                    continue
                if udlr != 0 and diagonal != 0:
                    synthesis_d = 1
                for _ in range(4):
                    temp[x][y].append((synthesis_m, synthesis_s, synthesis_d))
                    synthesis_d += 2
    grid = temp


dirs = ((-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1))  # ↑, ↗, →, ↘, ↓, ↙, ←, ↖
N, M, K = map(int, input().split())
grid = [[[] for _ in range(N)] for _ in range(N)]
for _ in range(M):
    x, y, m, s, d = map(int, input().split())
    grid[x - 1][y - 1].append((m, s, d))
for _ in range(K):
    atoms_move()
    atoms_synthesis()
result = 0
for x in range(N):
    for y in range(N):
        while grid[x][y]:
            m, _, _ = grid[x][y].pop()
            result += m
print(result)