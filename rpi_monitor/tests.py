
def fibonacci_test(n):
    while True:
        result=fibonacci(n)

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
