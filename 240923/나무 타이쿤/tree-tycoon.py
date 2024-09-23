from collections import deque


def move_supplements(d, p):
    global supplements
    temp = []
    dx, dy = move_dirs[d - 1]
    for x, y in supplements:
        nx = (x + dx * p) % n
        ny = (y + dy * p) % n
        temp.append((nx, ny))
    supplements = temp


def inject_supplements_and_growth():
    global tree_heights
    for x, y in supplements:
        tree_heights[x][y] += 1
    for x, y in supplements:
        for dx, dy in tree_dirs:
            nx = x + dx
            ny = y + dy
            if 0 <= nx < n and 0 <= ny < n and 1 <= tree_heights[nx][ny]:
                tree_heights[x][y] += 1


def cut_trees_and_add_supplements():
    global supplements, tree_heights
    temp = []
    for x in range(n):
        for y in range(n):
            if (x, y) not in supplements and 2 <= tree_heights[x][y]:
                tree_heights[x][y] -= 2
                temp.append((x, y))
    supplements = temp


move_dirs = ((0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (1, 1))  # → ↗ ↑ ↖ ← ↙ ↓ ↘
tree_dirs = ((-1, -1), (-1, 1), (1, 1), (1, -1))  # 나무 대각선
n, m = map(int, input().split())
supplements = [[0] * n for _ in range(n)]
tree_heights = [list(map(int, input().split())) for _ in range(n)]
move_rules = deque([tuple(map(int, input().split())) for _ in range(m)])
supplements = [(n - 1, 0), (n - 1, 1), (n - 2, 0), (n - 2, 1)]
for _ in range(m):
    d, p = move_rules.popleft()
    move_supplements(d, p)
    inject_supplements_and_growth()
    cut_trees_and_add_supplements()
result = 0
for th in tree_heights:
    result += sum(th)
print(result)