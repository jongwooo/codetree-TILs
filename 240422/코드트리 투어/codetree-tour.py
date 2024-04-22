import sys
import heapq


def init(n, m, vertex_info):
    global graph, cost, product, for_sale, cancel, starting_point, size
    graph = [[] for _ in range(n)]
    for v, u, w in vertex_info:
        graph[v].append((u, w))
        graph[u].append((v, w))
    starting_point = 0
    size = n
    cost = dijkstra()
    product = []
    for_sale = [False] * 30_005
    cancel = [False] * 30_005


def add_product(idx, revenue, dest):
    global for_sale
    for_sale[idx] = True
    heapq.heappush(product, ((revenue - cost[dest]) * -1, idx, revenue, dest))


def cancel_product(idx):
    global cancel
    if for_sale[idx]:
        cancel[idx] = True


def sell_optimal_product():
    while product:
        p = product[0]
        if p[0] > 0:
            break
        heapq.heappop(product)
        if not cancel[p[1]]:
            return p[1]
    return -1


def move_starting_point(point):
    global starting_point, cost, product
    starting_point = point
    cost = dijkstra()
    product = renew()


def renew():
    renewed = []
    while product:
        _, idx, revenue, dest = heapq.heappop(product)
        heapq.heappush(renewed, ((revenue - cost[dest]) * -1, idx, revenue, dest))
    return renewed


def dijkstra():
    queue = []
    distance = [INF] * size
    distance[starting_point] = 0
    heapq.heappush(queue, (0, starting_point))
    while queue:
        dist, now = heapq.heappop(queue)
        if distance[now] < dist:
            continue
        for next_node, next_dist in graph[now]:
            new_dist = dist + next_dist
            if new_dist < distance[next_node]:
                distance[next_node] = new_dist
                heapq.heappush(queue, (new_dist, next_node))
    return distance


INIT = 100
ADD_PRODUCT = 200
CANCEL_PRODUCT = 300
SELL_OPTIMAL_PRODUCT = 400
MOVE_STARTING_POINT = 500
INF = int(1e9)

Q = int(sys.stdin.readline())
graph = []
cost = []
product = []
for_sale = []
cancel = []
starting_point = 0
size = 0
for _ in range(Q):
    command = list(map(int, sys.stdin.readline().split()))
    if command[0] == INIT:
        v_info = []
        for i in range(3, len(command), 3):
            v_info.append((command[i], command[i + 1], command[i + 2]))
        init(command[1], command[2], v_info)
    elif command[0] == ADD_PRODUCT:
        add_product(command[1], command[2], command[3])
    elif command[0] == CANCEL_PRODUCT:
        cancel_product(command[1])
    elif command[0] == SELL_OPTIMAL_PRODUCT:
        product_id = sell_optimal_product()
        print(product_id)
    elif command[0] == MOVE_STARTING_POINT:
        move_starting_point(command[1])