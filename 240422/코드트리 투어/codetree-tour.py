import sys
import heapq

INF = int(1e9)
starting_point = 0
graph = []
distance = []
products = dict()


def init(n, m, vertex_info):
    global starting_point, graph, distance, products
    starting_point = 0
    graph = [[] for _ in range(n)]
    distance = [INF] * n
    for v, u, w in vertex_info:
        graph[v].append((u, w))
        graph[u].append((v, w))
    products = dict()
    dijkstra()


def add_product(idx, revenue, dest):
    global products
    products[idx] = (revenue, dest)


def cancel_product(idx):
    global products
    if idx in products:
        del products[idx]


def sell_optimal_product():
    product_candidates = []
    for idx, product in products.items():
        revenue, dest = product
        cost = distance[dest]
        if cost == INF:
            continue
        if revenue < cost:
            continue
        heapq.heappush(product_candidates, (-(revenue - cost), idx))
    if not product_candidates:
        return -1
    _, optimal_idx = heapq.heappop(product_candidates)
    cancel_product(optimal_idx)
    return optimal_idx


def move_starting_point(s):
    global starting_point
    starting_point = s
    dijkstra()


def dijkstra():
    queue = []
    heapq.heappush(queue, (0, starting_point))
    distance[starting_point] = 0
    while queue:
        cost, now = heapq.heappop(queue)
        if distance[now] < cost:
            continue
        for next_node, next_cost in graph[now]:
            new_cost = cost + next_cost
            if new_cost < distance[next_node]:
                distance[next_node] = new_cost
                heapq.heappush(queue, (new_cost, next_node))


INIT = 100
ADD_PRODUCT = 200
CANCEL_PRODUCT = 300
SELL_OPTIMAL_PRODUCT = 400
MOVE_STARTING_POINT = 500

Q = int(sys.stdin.readline())
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