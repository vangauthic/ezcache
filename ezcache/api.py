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
            
        if self.cache_type == 'dict':
            return (time.time() - self.timestamps[key]) > self.timeout
        else:
            try:
                return (time.time() - self.timestamps[key]) > self.timeout
            except IndexError:
                return False

    def _remove_expired(self):
        if self.timeout is None:
            return False
        
        if self.cache_type == 'dict':
            keys_to_remove = [k for k in list(self.cache.keys()) if self._is_expired(k)]
            for key in keys_to_remove:
                del self.cache[key]
                del self.timestamps[key]
        else:
            indices_to_remove = [i for i in range(len(self.cache)-1, -1, -1) 
                                if self._is_expired(i)]
            for i in indices_to_remove:
                self.cache.pop(i)
                self.timestamps.pop(i)

    def set(self, key, **kwargs):
        self._remove_expired()
        
        if self.cache_type == 'dict':
            value = kwargs.get('value', None)
            
            # Handle max items - remove oldest first
            if self.max_items and len(self.cache) >= self.max_items and key not in self.cache:
                # Remove oldest item (first item in OrderedDict)
                oldest_key, _ = next(iter(self.cache.items()))
                del self.cache[oldest_key]
                del self.timestamps[oldest_key]
            
            # Update or add new item
            if key in self.cache:
                del self.cache[key]
                del self.timestamps[key]
            self.cache[key] = value
            self.timestamps[key] = time.time()
        else:
            # List cache implementation
            value = key  # For lists, the input key is the value to store
            
            # Handle max items limit
            if self.max_items and len(self.cache) >= self.max_items:
                self.cache.pop(0)  # Remove oldest item
                self.timestamps.pop(0)  # Remove oldest timestamp
            
            # Add new value and timestamp
            self.cache.append(value)
            self.timestamps.append(time.time())

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