import asyncio
import time
from ezcache.api import EZCache

async def main():
    cache = EZCache(cache_type='dict', max_items=3, timeout=5)
    try:
        cache.set('a', 1)
        cache.set('b', 2)
        print(cache.get('a'))

        time.sleep(6)
        print(cache.get('a'))
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    asyncio.run(main())