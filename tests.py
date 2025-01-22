import asyncio
import time
from ezcache.api import EZCache

async def main():
    try:
        def measure_time(func):
            start = time.perf_counter()
            result = func()
            end = time.perf_counter()
            return result, (end - start) * 1000

        print("\n=== Testing Dict Cache ===")
        dict_cache = EZCache(cache_type='dict', max_items=3, timeout=5)
        
        # Test max items
        print("\nTesting max_items (FIFO):")
        result, duration = measure_time(lambda: dict_cache.set('a', value=1))
        print(f"Added a=1: {dict_cache.view_all()} (took {duration:.2f} ms)")
        result, duration = measure_time(lambda: dict_cache.set('b', value=2))
        print(f"Added b=2: {dict_cache.view_all()} (took {duration:.2f} ms)")
        result, duration = measure_time(lambda: dict_cache.set('c', value=3))
        print(f"Added c=3: {dict_cache.view_all()} (took {duration:.2f} ms)")
        result, duration = measure_time(lambda: dict_cache.set('d', value=4))
        print(f"Added d=4 (should remove a): {dict_cache.view_all()} (took {duration:.2f} ms)")
        
        # Test timeout
        print("\nTesting timeout:")
        new_cache = EZCache(cache_type='dict', max_items=3, timeout=2)
        result, duration = measure_time(lambda: new_cache.set('x', value=100))
        print(f"Before timeout: {new_cache.view_all()} (took {duration:.2f} ms)")
        time.sleep(3)
        print("After timeout:", new_cache.view_all())
        
        print("\n=== Testing List Cache ===")
        list_cache = EZCache(cache_type='list', max_items=3, timeout=5)
        
        # Test max items for list
        print("\nTesting list max_items (FIFO):")
        result, duration = measure_time(lambda: list_cache.set(1))
        print(f"Added 1: {list_cache.view_all()} (took {duration:.2f} ms)")
        result, duration = measure_time(lambda: list_cache.set(2))
        print(f"Added 2: {list_cache.view_all()} (took {duration:.2f} ms)")
        result, duration = measure_time(lambda: list_cache.set(3))
        print(f"Added 3: {list_cache.view_all()} (took {duration:.2f} ms)")
        result, duration = measure_time(lambda: list_cache.set(4))
        print(f"Added 4 (should remove 1): {list_cache.view_all()} (took {duration:.2f} ms)")

        # Test list timeout
        print("\nTesting list timeout:")
        list_timeout_cache = EZCache(cache_type='list', max_items=3, timeout=2)
        result, duration = measure_time(lambda: list_timeout_cache.set(100))
        print(f"Before timeout: {list_timeout_cache.view_all()} (took {duration:.2f} ms)")
        time.sleep(3)
        print("After timeout:", list_timeout_cache.view_all())
        
    except Exception as e:
        print(f"Error: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(main())