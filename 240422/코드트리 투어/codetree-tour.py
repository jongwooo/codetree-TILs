import sys
import heapq

INF = int(1e9)
starting_point = 0
graph = []
products = dict()


def init(n, m, vertex_info):
    global graph, products
    graph = [[INF] * n for _ in range(n)]
    for i in range(n):
        graph[i][i] = 0
    for v, u, w in vertex_info:
        if graph[v][u] > w:
            graph[v][u] = w
            graph[u][v] = w
    for k in range(n):
        for a in range(n):
            for b in range(n):
                if graph[a][b] > graph[a][k] + graph[k][b]:
                    graph[a][b] = graph[a][k] + graph[k][b]
    products = dict()


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
        cost = graph[starting_point][dest]
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