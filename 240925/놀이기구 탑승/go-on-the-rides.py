def find_seat(student):
    global grid
    candidates = []
    for x in range(n):
        for y in range(n):
            if not grid[x][y]:
                favorite_friends_cnt = count_favorite_friends(student, x, y)
                empty_seats_cnt = count_empty_seats(x, y)
                candidates.append((-favorite_friends_cnt, -empty_seats_cnt, y, x))
    candidates.sort()
    _, _, y, x = candidates[0]
    grid[x][y] = student


def count_favorite_friends(student, x, y):
    favorite_friends_cnt = 0
    for dx, dy in dirs:
        nx = x + dx
        ny = y + dy
        if 0 <= nx < n and 0 <= ny < n and grid[nx][ny] > 0:
            if grid[nx][ny] in favorite_friend_infos[student]:
                favorite_friends_cnt += 1
    return favorite_friends_cnt


def count_empty_seats(x, y):
    empty_seats_cnt = 0
    for dx, dy in dirs:
        nx = x + dx
        ny = y + dy
        if 0 <= nx < n and 0 <= ny < n and not grid[nx][ny]:
            empty_seats_cnt += 1
    return empty_seats_cnt


dirs = ((-1, 0), (0, 1), (1, 0), (0, -1))
scores = (0, 1, 10, 100, 1_000)
n = int(input())
grid = [[0] * n for _ in range(n)]
favorite_friend_infos = [[] for _ in range(n ** 2 + 1)]
for _ in range(n ** 2):
    n0, *favorite_friends = map(int, input().split())
    favorite_friend_infos[n0] = list(favorite_friends)
    find_seat(n0)
score = 0
for i in range(n):
    for j in range(n):
        score += scores[count_favorite_friends(grid[i][j], i, j)]
print(score)