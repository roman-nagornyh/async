import sys
from time import perf_counter
from typing import NamedTuple, Generator
from multiprocessing import (
    Process,
    SimpleQueue,
    cpu_count
)                                                               # 1
from multiprocessing import queues                              # 2
from healthy_sleep import is_prime_sync

NUMBERS = (i for i in range(2, 1000))


class PrimeResult(NamedTuple):                                  # 3
    n: int
    prime: bool
    elapsed: float


JobQueue = queues.SimpleQueue[int]                              # 4
ResultQueue = queues.SimpleQueue[PrimeResult]                   # 5


def check(n: int) -> PrimeResult: #6
    t0 = perf_counter()
    res = is_prime_sync(n)
    return PrimeResult(n, res, perf_counter() - t0)


def worker(jobs: JobQueue, results: ResultQueue): #7
    while n := jobs.get(): #8
        results.put(check(n)) #9
    results.put(PrimeResult(0, False, 0.0)) #10


def start_jobs(procs: int, jobs: JobQueue, results: ResultQueue) -> None: #11
    for n in NUMBERS:
        jobs.put(n) #12
    for _ in range(procs):
        proc = Process(target=worker, args=(jobs, results)) #13
        proc.start() #14
        jobs.put(0) #15


def main() -> None:
    if len(sys.argv) < 2:
        procs = cpu_count()
    else:
        procs = int(sys.argv[1])
    t0 = perf_counter()
    jobs: JobQueue = SimpleQueue()
    results: ResultQueue = SimpleQueue()
    start_jobs(procs, jobs, results)
    checked = report(procs, results)
    elapsed = perf_counter() - t0
    print(f'{checked} checks in {elapsed:.2f}s')


def report(procs: int, results: ResultQueue):
    checked = 0
    procs_done = 0
    while procs_done < procs:
        n, prime, elapsed = results.get()
        if n == 0:
            procs_done += 1
        else:
            checked += 1
            label = 'P' if prime else ' '
            print(f'{n:16}{label} {elapsed:9.6f}s')
    return checked


main()
