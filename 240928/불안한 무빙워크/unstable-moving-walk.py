from collections import deque


def test_moving_work():
    global durability_zero_cnt
    # 무빙워크가 한 칸 회전한다
    moving_work.appendleft(moving_work.pop())
    person.appendleft(person.pop())
    # n번 칸에 사람이 있으면 내린다
    if person[n - 1]:
        person[n - 1] = 0
    # 무빙워크가 회전하는 방향으로 한 칸 이동할 수 있으면 이동한다
    for i in range(n - 1, 0, -1):
        if person[i - 1] and not person[i] and moving_work[i] > 0:
            person[i - 1], person[i] = person[i], person[i - 1]
            moving_work[i] -= 1
            if moving_work[i] == 0:
                durability_zero_cnt += 1
    # n번 칸에 사람이 있으면 내린다
    if person[n - 1]:
        person[n - 1] = 0
    # 1번 칸에 사람이 없고 안정성이 0이 아니라면 사람을 한 명 더 올린다
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