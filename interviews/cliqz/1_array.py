

def solution(A):
    current = 0
    jumps = 0
    while True:
        if A[current] == 0:
            return -1

        prev = current
        current += A[current]
        A[prev] = 0
        jumps += 1

        if current < 0 or current >= len(A):
            return jumps
