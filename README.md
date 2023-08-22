# Caching 

A cache implementation designed in python to store key-value pairs with a maximum size limit and [LRU](https://en.wikipedia.org/wiki/Cache_replacement_policies) (Least Recently Used) eviction strategy. The cache also provides additional features like filtering keys and basic thread-safety using locks.

# Features

1. Maximum cache size enforcement

2. Supporting CRUD operations

3. Filter operations supported for data types such as string, int, list and also regex match.
   
4. Cache Implementation : LRU
   
5. Thread safe


# Requirements
python >= 3.7

# Quickstart
Let's start with some basic caching by creating a cache object:

```
from cache import Cache

cache = Cache()
```

By default the cache object will have a maximum size of 256
```
cache = Cache(maxsize=256)
```
Set a cache key using cache.set():

```
cache.set(1, 'foobar')

```
Get a cache key using cache.get():

```
assert cache.get(1) == 'foobar'
```

Get a default value when cache key isn't set:

```
assert cache.get(2) is None
```
Update the value using cache.update():
```
cache.update(1,'Hello')
assert cache.update(1) == 'Hello' (True)
```
Delete the value using cache.delete():
```
cache.delete(1)
assert cache.get(1) == None
```

Filter the cache when key is list of strings
```
cache.add("key1", "value1")
cache.add("key2", "value2")
cache.add("key3", "value3")

filtered_values = cache.filter(["key1", "key2"])
expected_values = [["key1", "value1"], ["key2", "value2"]]
self.assertEqual(filtered_values, expected_values) -> True
```

Filter the cache when key is pattern matching
```
cache.add("key1", "value1")
cache.add("key2", "value2")

filtered_values = cache._filter_keys("key*")
expected_values = [("key1", "value1"), ("key2", "value2")]
self.assertEqual(filtered_values, expected_values) -> True

cache.add("apple", "fruit")
cache.add("banana", "fruit")
cache.add("carrot", "vegetable")

pattern = re.compile(r"^(app|ban)")
filtered_items = self.cache._filter_keys(pattern)
expected_items = [("apple", "fruit"), ("banana", "fruit")]
self.assertEqual(filtered_items, expected_items) -> True

```

Filter the cache when key is string
```
cache.add("key1", "value1")
cache.add("key2", "value2")

filtered_values = cache._filter_keys("key1")
expected_values = [("key1", "value1")]
self.assertEqual(filtered_values, expected_values) -> True
```

Cache Eviction when you add more than cache length
```
cache = Cache(3)

cache.add("key1", "value1")
cache.add("key2", "value2")
cache.add("key3", "value3")
cache.add("key4", "value4")

self.assertIsNone(cache.get("key1))

```