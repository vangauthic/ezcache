import asyncio
import time
from ezcache.api import EZCache

async def main():
    cache = EZCache(cache_type='dict', max_items=3, timeout=None)
    cache2 = EZCache(cache_type='list', max_items=3, timeout=5)
    try:
        cache.set('a', value=1)
        cache.set('b', value=2)
        cache.set('c', value=3)
        cache2.set(1)
        print(cache.view_all())
        cache.set('d', value=4)
        print(cache.view_all())


        time.sleep(6)
        print(cache.get('b'))
        print(cache2.get(1))
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    asyncio.run(main())