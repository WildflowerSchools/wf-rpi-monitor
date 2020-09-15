
import multiprocessing
import time
import logging

logger = logging.getLogger(__name__)

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

def sleep_test(delay=5, num_processes=None, parallel=True, log_level=None):
    if log_level is not None:
        numeric_log_level = getattr(logging, log_level.upper(), None)
        if not isinstance(numeric_log_level, int):
            raise ValueError('Invalid log level: %s'.format(log_level))
        logging.basicConfig(level=numeric_log_level)
    if parallel:
        if num_processes is None:
            num_cpus = multiprocessing.cpu_count()
            logger.info('Number of processes not specified. Defaulting to {}'.format(num_cpus))
            num_processes = num_cpus
        with multiprocessing.Pool(num_processes) as p:
            _ = list(p.imap(sleep, infinite_generator(delay), chunksize=1))
    else:
        _ = list(map(sleep, infinite_generator(delay)))

def sleep(delay):
    logger.info('Test launched. Sleeping for {} seconds'.format(delay))
    print('Test launched. Sleeping for {} seconds'.format(delay))
    time.sleep(delay)

def infinite_generator(x):
    while True:
        yield x
