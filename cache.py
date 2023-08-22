from collections import OrderedDict
from threading import RLock
import logging
import typing as t
import re
import fnmatch

class Cache:
    def __init__(self, maxsize: int = 256):
        """
        Initializes a caching mechanism with an OrderedDict to store cache entries.
        The maxsize parameter defines the maximum number of entries the cache can hold.

        :param maxsize: Maximum size of cache dictionary. Defaults to 256.
        """
        self.maxsize = maxsize
        self.cache = OrderedDict()
        self.lock = RLock()

    def keys(self):
        """
        Returns a list of keys stored in the cache.
        """
        return self.cache.keys()

    def values(self):
        """
        Returns a list of values stored in the cache.
        """
        return self.cache.values()

    def clear(self):
        """
        Clears all entries from the cache.
        """
        with self.lock:
            self.cache.clear()

    def add(self, key, value):
        """
        Adds a key-value pair to the cache. If the cache is full, evicts the least recently used entry.

        :param key: The key to add.
        :param value: The value associated with the key.
        """
        with self.lock:
            self._add(key, value)

    def _add(self, key, value):
        """
        Internal method to add a key-value pair to the cache.

        :param key: The key to add.
        :param value: The value associated with the key.
        """
        self._evict_if_full()
        self.cache[key] = value

    def _evict_if_full(self):
        """
        Internal method to evict the least recently used entry if the cache is full.
        """
        if len(self.cache) == self.maxsize:
            self.cache.popitem(last=False)

    def get(self, key):
        """
        Retrieves a value from the cache based on the provided key.
        Moves the retrieved entry to the end to mark it as most recently used.

        :param key: The key of the value to retrieve.
        :return: The value associated with the key, or None if not found.
        """
        with self.lock:
            return self._get(key)

    def _get(self, key):
        """
        Internal method to retrieve a value from the cache based on the provided key.
        Moves the retrieved entry to the end to mark it as most recently used.

        :param key: The key of the value to retrieve.
        :return: The value associated with the key, or None if not found.
        """
        try:
            value = self.cache.pop(key)
            self.cache[key] = value
        except KeyError:
            self._log_error(f"Key {key} not found in the cache")
            return None
        return value


    def update(self, key, value):
        """
        Updates the value associated with the provided key in the cache.

        :param key: The key of the value to update.
        :param value: The new value to associate with the key.
        """
        with self.lock:
            self._update(key, value)

    def _update(self, key, value):
        """
        Internal method to update the value associated with the provided key in the cache.
        If the key exists, updates the value; otherwise, logs an error and adds the key-value pair.

        :param key: The key of the value to update.
        :param value: The new value to associate with the key.
        """
        if self._key_exists(key):
            del self.cache[key]
            self.cache[key] = value
        else:
            self._log_error(f"Key {key} not present in the cache")
            self.cache[key] = value

    def delete(self, key):
        """
        Deletes the value associated with the provided key from the cache.

        :param key: The key of the value to delete.
        :return: The number of deleted entries (0 or 1).
        """
        with self.lock:
            return self._delete(key)

    def _delete(self, key):
        """
        Internal method to delete the value associated with the provided key from the cache.

        :param key: The key of the value to delete.
        :return: The number of deleted entries (0 or 1).
        """
        if self._key_exists(key):
            del self.cache[key]
            return 1
        else:
            self._log_error(f"Key {key} trying to delete not present in the cache")
            return 0

    def filter(self, key):
        """
        Retrieves the value associated with the provided key from the cache.

        :param key: The key of the value to retrieve.
        :return: The value associated with the key, or None if key is not found.
        """
        with self.lock:
            return self._filter_keys(key)

    
    def _filter_keys(self, iteratee):
        """
        Filters the cache keys based on the provided iteratee, 
        which can be a string, int, list, regex match or iterable.

        :param iteratee: The filtering condition.
        :return: List of values corresponding to filtered keys.
        """

        target = self.cache

        if isinstance(iteratee, str):
            filter_by = re.compile(fnmatch.translate(iteratee)).match
        elif isinstance(iteratee, int):
            target = [(iteratee, self.cache[iteratee]) for iteratee in target]
        elif isinstance(iteratee, t.Pattern):
            filter_by = iteratee.match
        else:
            target = iteratee

            def filter_by(key): 
                return key in self.cache

        return [(key, self.cache.get(key, "Key not present in cache")) for key in target if filter_by(key)]

        

    def _key_exists(self, key):
        """
        Checks if a key exists in the cache.

        :param key: The key to check.
        :return: True if the key exists, False otherwise.
        """
        return key in self.cache

    def _log_error(self, message):
        """
        Logs an error message.

        :param message: The error message to log.
        """
        logging.error(message)