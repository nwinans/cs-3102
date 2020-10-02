from timeit import timeit
def theta_time(n):
    num = 1
    for _ in range(n):
        num = ~ num
    return num

def wrapper(func, *args, **kwargs):
    def wrapped():
        return func(*args, **kwargs)
    return wrapped

num_range = [10**i for i in range(1,7)]
for num in num_range:
    print(float(timeit(wrapper(theta_time, num), number=1000)) / num)