import time
import functools
import psutil
import os
from contextlib import contextmanager

def measure_performance_decorator(func):
    """Decorator to measure execution time and memory usage of a function."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        process = psutil.Process(os.getpid())
        mem_before = process.memory_info().rss / (1024 * 1024) # MB
        
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        
        mem_after = process.memory_info().rss / (1024 * 1024) # MB
        
        latency = end_time - start_time
        mem_diff = mem_after - mem_before
        
        print(f"[{func.__name__}] Latency: {latency:.4f} seconds | Memory diff: {mem_diff:.4f} MB")
        return result
    return wrapper

@contextmanager
def measure_performance_context(name="Block"):
    """Context manager to measure execution time and memory usage of a block of code."""
    process = psutil.Process(os.getpid())
    mem_before = process.memory_info().rss / (1024 * 1024) # MB
    
    start_time = time.perf_counter()
    yield
    end_time = time.perf_counter()
    
    mem_after = process.memory_info().rss / (1024 * 1024) # MB
    
    latency = end_time - start_time
    mem_diff = mem_after - mem_before
    
    print(f"[{name}] Latency: {latency:.4f} seconds | Memory diff: {mem_diff:.4f} MB")
