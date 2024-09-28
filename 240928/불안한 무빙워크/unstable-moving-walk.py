from collections import deque


def test_moving_work():
    global durability_zero_cnt
    # 무빙워크가 한 칸 회전한다
    moving_work.appendleft(moving_work.pop())
    person.appendleft(person.pop())
    if person[n - 1]:
        person[n - 1] = 0
    for i in range(n - 1, 0, -1):
        if person[i - 1] and not person[i] and moving_work[i] > 0:
            person[i - 1], person[i] = person[i], person[i - 1]
            moving_work[i] -= 1
            if moving_work[i] == 0:
                durability_zero_cnt += 1
    if not person[0] and moving_work[0] > 0:
        person[0] = 1
        moving_work[0] -= 1
        if moving_work[0] == 0:
            durability_zero_cnt += 1


n, k = map(int, input().split())
durability = list(map(int, input().split()))
moving_work = deque(durability)
person = deque([0 for i in range(2 * n)])
test_cnt = 0
durability_zero_cnt = 0
while True:
    test_moving_work()
    test_cnt += 1
    if k <= durability_zero_cnt:
        break
print(test_cnt)