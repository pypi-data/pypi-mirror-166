#!/usr/bin/env python3
import os
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed


class Process:
    def __init__(self, func, args=[]):
        self.func = func
        self.args = args

    def run(self):
        return self.func(*self.args)


def multi_run(processes=[], threads=0):
    threads = os.cpu_count() if threads <= 0 else int(threads)

    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = []
        for p in processes:
            future = executor.submit(p.func, *p.args)
            futures.append(future)

        results = [future.result() for future in as_completed(futures)]

    return results
