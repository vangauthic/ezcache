import time
from collections import OrderedDict
from ._types import *

class EZCache():
    def __init__(self, cache_type='dict', max_items=None, timeout=None):
        if cache_type not in ['dict', 'list']:
            raise ValueError("cache_type must be either 'dict' or 'list'")
        
        self.cache_type = cache_type
        self.max_items = max_items
        self.timeout = timeout
        self.cache = OrderedDict() if cache_type == 'dict' else []
        self.timestamps = {} if cache_type == 'dict' else []

    def _is_expired(self, key):
        if self.timeout is None:
            return False
        return (time.time() - self.timestamps[key]) > self.timeout

    def _remove_expired(self):
        keys_to_remove = []
        for key in self.cache if self.cache_type == 'dict' else range(len(self.cache)):
            if self._is_expired(key):
                keys_to_remove.append(key)
        for key in keys_to_remove:
            self.remove(key)

    def set(self, key, value):
        self._remove_expired()
        
        if self.cache_type == 'dict':
            if key in self.cache:
                self.cache.move_to_end(key)
            self.cache[key] = value
            self.timestamps[key] = time.time()
        else:
            if key in self.cache:
                self.cache.remove(key)
            self.cache.append((key, value))
            self.timestamps.append(time.time())

        if self.max_items is not None and len(self.cache) > self.max_items:
            self.remove(self.cache.popitem(last=False)[0] if self.cache_type == 'dict' else self.cache.pop(0)[0])

    def get(self, key):
        self._remove_expired()
        
        if self.cache_type == 'dict':
            if key in self.cache and not self._is_expired(key):
                self.cache.move_to_end(key)
                return self.cache[key]
        else:
            for i, (k, v) in enumerate(self.cache):
                if k == key and not self._is_expired(i):
                    self.cache.append(self.cache.pop(i))
                    return v
        return None

    def remove(self, key):
        if self.cache_type == 'dict':
            if key in self.cache:
                del self.cache[key]
                del self.timestamps[key]
        else:
            for i, (k, _) in enumerate(self.cache):
                if k == key:
                    self.cache.pop(i)
                    self.timestamps.pop(i)
                    break

    def clear(self):
        self.cache = OrderedDict() if self.cache_type == 'dict' else []
        self.timestamps = {} if self.cache_type == 'dict' else []