# EZCache

EZCache is a Python library to easily create and manage list/dict caches with support for expiration and maximum item limits.

## Installation

```bash
pip install ezcache
```

## Quick Start

```python
import asyncio
from ezcache import EZCache

async def main():
    # Initialize dict cache
    dict_cache = EZCache(cache_type='dict', max_items=3, timeout=5)
    dict_cache.set('a', value=1)
    dict_cache.set('b', value=2)
    print(dict_cache.get('a'))  # Output: 1

    # Initialize list cache
    list_cache = EZCache(cache_type='list', max_items=3, timeout=5)
    list_cache.set(1)
    list_cache.set(2)
    print(list_cache.get(1))  # Output: 1

    # View all values in caches
    print(dict_cache.view_all())  # Output: {'a': 1, 'b': 2}
    print(list_cache.view_all())  # Output: [1, 2]

asyncio.run(main())
```

## Features
- Support for both dict and list caches
- Expiration of cache items based on timeout
- Maximum item limit for caches
- Methods to set, get, remove, and clear cache items
- Method to view all values in the cache

## License

This project is licensed under the MIT License - see the LICENSE file for details.
