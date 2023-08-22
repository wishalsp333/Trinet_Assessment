import unittest
from unittest.mock import patch
from cache import Cache
import re

class TestCache(unittest.TestCase):

    def setUp(self):
        self.cache = Cache(maxsize=3)

    def test_add_and_get(self):
        self.cache.add("key1", "value1")
        self.cache.add("key2", "value2")

        self.assertEqual(self.cache.get("key1"), "value1")
        self.assertEqual(self.cache.get("key2"), "value2")
        self.assertIsNone(self.cache.get("key3"))

    def test_update_existing_key(self):
        self.cache.add("key1", "value1")
        self.cache.update("key1", "new_value")
        self.assertEqual(self.cache.get("key1"), "new_value")

    def test_update_nonexistent_key(self):
        self.cache.update("key1", "value1")
        self.assertIsNone(self.cache.get("key"))

    def test_delete_existing_key(self):
        self.cache.add("key1", "value1")
        count = self.cache.delete("key1")

        self.assertEqual(count, 1)
        self.assertIsNone(self.cache.get("key1"))

    def test_delete_nonexistent_key(self):
        count = self.cache.delete("key1")

        self.assertEqual(count, 0)

    def test_filter_by_string(self):
        self.cache.add("key1", "value1")
        self.cache.add("key2", "value2")
        self.cache.add("key3", "value3")

        filtered_value = self.cache.filter("key2")
        self.assertEqual(filtered_value, [("key2", "value2")])

    def test_filter_by_list(self):
        self.cache.add("key1", "value1")
        self.cache.add("key2", "value2")
        self.cache.add("key3", "value3")

        filtered_values = self.cache.filter(["key1", "key3"])
        expected_values = [["key1", "value1"], ["key3", "value3"]]
        self.assertEqual(filtered_values, expected_values)

    def test_keys(self):
        self.cache.add("key1", "value1")
        self.cache.add("key2", "value2")

        keys = self.cache.keys()
        self.assertEqual(list(keys), ["key1", "key2"])

    def test_values(self):
        self.cache.add("key1", "value1")
        self.cache.add("key2", "value2")

        values = self.cache.values()
        self.assertEqual(list(values), ["value1", "value2"])

    def test_clear(self):
        self.cache.add("key1", "value1")
        self.cache.add("key2", "value2")

        self.cache.clear()

        keys = self.cache.keys()
        self.assertEqual(list(keys), [])
    
    def test_filter_by_string_exact_match(self):
        self.cache.add("key1", "value1")
        self.cache.add("key2", "value2")
        self.cache.add("key3", "value3")

        filtered_values = self.cache._filter_keys("key2")
        expected_values = [("key2", "value2")]
        self.assertEqual(filtered_values, expected_values)

    def test_filter_by_string_pattern_match(self):
        self.cache.add("key1", "value1")
        self.cache.add("key2", "value2")
        self.cache.add("key3", "value3")

        filtered_values = self.cache._filter_keys("key*")
        expected_values = [("key1", "value1"), ("key2", "value2"), ("key3", "value3")]
        self.assertEqual(filtered_values, expected_values)

    def test_filter_by_pattern(self):
        self.cache.add("apple", "fruit")
        self.cache.add("banana", "fruit")
        self.cache.add("carrot", "vegetable")

        pattern = re.compile(r"^(app|ban)")
        filtered_items = self.cache._filter_keys(pattern)
        expected_items = [("apple", "fruit"), ("banana", "fruit")]
        self.assertEqual(filtered_items, expected_items)

    def test_filter_by_list(self):
        self.cache.add("key1", "value1")
        self.cache.add("key2", "value2")
        self.cache.add("key3", "value3")

        filtered_values = self.cache._filter_keys(["key1", "key3"])
        expected_values = [("key1", "value1"), ("key3", "value3")]
        self.assertEqual(filtered_values, expected_values)

    def test_filter_empty_cache(self):
        filtered_values = self.cache._filter_keys("key1")

        self.assertEqual(filtered_values, [])

    def test_filter_not_found(self):
        self.cache.add("key1", "value1")
        self.cache.add("key2", "value2")

        filtered_values = self.cache._filter_keys("key3")
        self.assertEqual(filtered_values, [])

    def test_filter_case_sensitive(self):
        self.cache.add("Key1", "value1")
        self.cache.add("key2", "value2")

        filtered_values = self.cache._filter_keys("Key1")
        expected_values = [("Key1", "value1")]
        self.assertEqual(filtered_values, expected_values)
    
    def test_eviction_cache(self):
        self.cache = Cache(maxsize=3)
        self.cache.add("Key1", "value1")
        self.cache.add("key2", "value2")
        self.cache.add("Key3", "value3")
        self.cache.add("key4", "value4")
    
        self.assertIsNone(self.cache.get("Key1"))

if __name__ == '__main__':
    unittest.main()
