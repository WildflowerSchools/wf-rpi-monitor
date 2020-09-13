
import multiprocessing

def fibonacci_test(n, num_processes=None):
    if num_processes is None:
        num_cpus = multiprocessing.cpu_count()
        print('Number of processes not specified. Defaulting to {}'.format(num_cpus))
        num_processes = num_cpus
    with multiprocessing.Pool(num_processes) as p:
        while True:
            result=p.apply_async(fibonacci, (n,))

def fibonacci(n):
    if n<2:
        return 1
    n1=1
    n2=1
    for i in range(2, n + 1):
        n = n1 + n2
        n1 = n2
        n2 = n
    return n
