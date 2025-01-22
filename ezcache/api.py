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
        self.index_map = {}
        
    def _is_expired(self, key):
        if self.timeout is None:
            return False
        return (time.time() - self.timestamps[key]) > self.timeout

    def _remove_expired(self):
        if self.timeout is None:
            return False
        keys_to_remove = []
        for key in self.cache if self.cache_type == 'dict' else range(len(self.cache)):
            if self._is_expired(key):
                keys_to_remove.append(key)
        for key in keys_to_remove:
            self.remove(key)

    def set(self, key, **kwargs):
        self._remove_expired()
        self.value = kwargs.get('value', None)
        
        if self.cache_type == 'dict':
            if key in self.cache:
                self.cache.move_to_end(key)
            self.cache[key] = self.value
            self.timestamps[key] = time.time()
        else:
            if key in self.cache:
                index = self.cache.index(key)
                self.cache.pop(index)
                self.timestamps.pop(index)
            self.cache.append(key)
            self.timestamps.append(time.time())

        if self.max_items is not None and len(self.cache) > self.max_items:
            if self.cache_type == 'dict':
                self.remove(self.cache.popitem(last=False)[0])
            else:
                self.remove(self.cache[0])

    def get(self, key):
        self._remove_expired()
        
        if self.cache_type == 'dict':
            if key in self.cache and not self._is_expired(key):
                self.cache.move_to_end(key)
                return self.cache[key]
        else:
            if key in self.index_map:  # O(1) lookup
                index = self.index_map[key]
                if not self._is_expired(index):
                    return self.cache.values()[key]
        return None

    def remove(self, key):
        if self.cache_type == 'dict':
            if key in self.cache:
                del self.cache[key]
                del self.timestamps[key]
        else:
            if key in self.index_map:  # O(1) lookup
                index = self.index_map[key]
                self.cache.pop(index)
                self.timestamps.pop(index)
                del self.index_map[key]
                # Update indices for remaining elements
                for k, idx in self.index_map.items():
                    if idx > index:
                        self.index_map[k] = idx - 1

    def clear(self):
        self.cache = OrderedDict() if self.cache_type == 'dict' else []
        self.timestamps = {} if self.cache_type == 'dict' else []

    def view_all(self):
        self._remove_expired()
        if self.cache_type == 'dict':
            return dict(self.cache.items())
        else:
            return list(self.cache)