import copy


def distance_from_maze_exit(people):
    global maze_exit
    row = abs(maze_exit[0] - people[0])
    column = abs(maze_exit[1] - people[1])
    d = max(row, column)
    r = min(maze_exit[0], people[0])
    c = min(maze_exit[1], people[1])
    if row < column:
        r = max(maze_exit[0], people[0]) - d
        if r < 0:
            r = 0
    elif column < row:
        c = max(maze_exit[1], people[1]) - d
        if c < 0:
            c = 0
    return d, r, c


def people_move():
    global distance_sum, peoples, maze_exit
    for pid, people in enumerate(peoples):
        r = maze_exit[0] - people[0]
        c = maze_exit[1] - people[1]
        if r != 0:
            dist = 1 if r > 0 else -1
            people_next = (people[0] + dist, people[1])
            if 0 <= people_next[0] < N and maze[people_next[0]][people_next[1]] == 0:
                peoples[pid] = people_next
                distance_sum += 1
                continue
        if c != 0:
            dist = 1 if c > 0 else -1
            people_next = (people[0], people[1] + dist)
            if 0 <= people_next[1] < N and maze[people_next[0]][people_next[1]] == 0:
                peoples[pid] = people_next
                distance_sum += 1


def rotate():
    global maze, peoples, maze_exit
    people_distances = []
    for people in peoples:
        people_distances.append(distance_from_maze_exit(people))
    people_distances.sort()
    d, r, c = people_distances[0]
    temp_maze = copy.deepcopy(maze)
    temp_peoples = []
    temp_exit = maze_exit
    for i in range(d + 1):
        for j in range(d + 1):
            if temp_maze[r + i][c + j] > 0:
                temp_maze[r + i][c + j] -= 1
            maze[r + j][c + d - i] = temp_maze[r + i][c + j]
            cur = (r + i, c + j)
            rotated = (r + j, c + d - i)
            while cur in peoples:
                peoples.remove(cur)
                temp_peoples.append(rotated)
            if cur == maze_exit:
                temp_exit = rotated
    peoples += temp_peoples
    maze_exit = temp_exit


N, M, K = map(int, input().split())
maze = [list(map(int, input().split())) for _ in range(N)]
peoples = [tuple(map(lambda x: int(x) - 1, input().split())) for _ in range(M)]
distance_sum = 0
maze_exit = tuple(map(lambda x: int(x) - 1, input().split()))
for _ in range(K):
    people_move()
    while maze_exit in peoples:
        peoples.remove(maze_exit)
    if not peoples:
        break
    rotate()
print(distance_sum)
print(maze_exit[0] + 1, maze_exit[1] + 1)