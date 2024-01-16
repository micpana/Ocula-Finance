import multiprocessing

def square(x):
    print(x[0])
    print(x[1])
    print(x[2])
    return x

if __name__ == '__main__':
    numbers = [1, 'b', [9,0,8]]
    pool = multiprocessing.Pool()
    results = pool.map(square, numbers)
    print(results)  # Output: [1, 4, 9, 16, 25]
