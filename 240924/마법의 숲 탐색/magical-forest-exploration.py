from collections import deque


def bfs(sx, sy):
    queue = deque([(sx, sy)])
    visited = [[False] * (C + 2) for _ in range(R + 4)]
    visited[sx][sy] = True
    max_row = 0
    while queue:
        x, y = queue.popleft()
        max_row = max(max_row, x)
        for dx, dy in exit_dirs:
            nx = x + dx
            ny = y + dy
            if not visited[nx][ny] and (grid[x][y] == grid[nx][ny] or ((x, y) in exit_set and grid[nx][ny] > 1)):
                queue.append((nx, ny))
                visited[nx][ny] = True
    return max_row - 2


R, C, K = map(int, input().split())
golem_infos = [tuple(map(int, input().split())) for _ in range(K)]
grid = [[1] + [0] * C + [1] for _ in range(R + 3)] + [[1] * (C + 2)]
exit_dirs = ((-1, 0), (0, 1), (1, 0), (0, -1))  # 북, 동, 남, 서
exit_set = set()
row_sum = 0
num = 2
for cy, d in golem_infos:
    cx = 1
    while True:
        if grid[cx + 1][cy - 1] + grid[cx + 2][cy] + grid[cx + 1][cy + 1] == 0:
            cx += 1
        elif grid[cx - 1][cy - 1] + grid[cx][cy - 2] + grid[cx + 1][cy - 1] \
                + grid[cx + 1][cy - 2] + grid[cx + 2][cy - 1] == 0:
            cx += 1
            cy -= 1
            d = (d - 1) % 4
        elif grid[cx + 1][cy + 1] + grid[cx][cy + 2] + grid[cx - 1][cy + 1] \
                + grid[cx + 1][cy + 2] + grid[cx + 2][cy + 1] == 0:
            cx += 1
            cy += 1
            d = (d + 1) % 4
        else:
            break
    if cx < 4:
        grid = [[1] + [0] * C + [1] for _ in range(R + 3)] + [[1] * (C + 2)]
        exit_set = set()
        continue
    grid[cx + 1][cy] = grid[cx - 1][cy] = num
    grid[cx][cy - 1:cy + 2] = [num] * 3
    num += 1
    exit_set.add((cx + exit_dirs[d][0], cy + exit_dirs[d][1]))
    row_sum += bfs(cx, cy)
print(row_sum)