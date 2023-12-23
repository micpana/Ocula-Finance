from collections import deque

ob = {
    'ls': deque([1, 2, 3, 4, 5])
}

print(ob['ls'][-1])