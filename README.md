# Cache Implementation in Python



- [Cache Implementation in Python](#cache-implementation-in-python)
  - [Introduction](#introduction)
  - [Installation](#installation)
  - [Features](#features)
  - [Cache Logic](#cache-logic)
    - [LRU (Least Recently Used) Eviction Strategy](#lru-least-recently-used-eviction-strategy)
    - [Thread-Safety](#thread-safety)
  - [General Workflow](#general-workflow)
  - [Unit Test Cases](#unit-test-cases)
    - [Test Case Descriptions](#test-case-descriptions)
  - [Summary](#summary)

## Introduction

This project presents a robust and efficient cache implementation in Python. Caching is a critical technique in computer science used to store frequently accessed data in order to reduce the time and resources required to retrieve it from the original source. This implementation is aimed at providing a versatile cache mechanism that can be easily integrated into various projects to improve performance.

## Installation

To use this cache implementation, follow these steps:

1. Clone the repository:

   bash
   git clone https://github.com/wishalsp333/Trinet_Assessment.git
   

2. Move the `cache.py` file into your project directory.

## Features

1. Maximum cache size enforcement

2. Supporting CRUD operations

3. Filter operations supported for data types such as string, int, list and also regex match.
   
4. Cache Implementation : LRU
   
5. Thread safe


## Cache Logic

### LRU (Least Recently Used) Eviction Strategy

The cache is implemented using an `OrderedDict`, which maintains the order of items based on their usage. The LRU eviction strategy ensures that the least recently used items are removed when the cache reaches its maximum capacity. This helps maintain the most relevant and frequently accessed data in the cache.

### Thread-Safety

The cache includes a `RLock` (Reentrant Lock) from the `threading` module to ensure thread-safety. This allows multiple threads to access the cache simultaneously while preventing data corruption or inconsistencies due to race conditions.

## General Workflow

1. Initialize the cache with a maximum size (default is 256).
2. Add key-value pairs to the cache using the `add` method.
3. Retrieve values from the cache using the `get` method.
4. Update existing values in the cache using the `update` method.
5. Delete values from the cache using the `delete` method.
6. Filter cache contents based on conditions using the `filter` method.
7. Retrieve lists of keys and values in the cache using the `keys` and `values` methods.
8. Clear all cache entries using the `clear` method.

## Unit Test Cases

Comprehensive unit test cases are provided in the `test.py` file. These test cases cover a wide range of scenarios to ensure the correctness and functionality of the Cache class. The test cases are structured to evaluate different cache operations, edge cases, and thread safety.

### Test Case Descriptions

The unit tests cover various aspects of the cache, including adding, retrieving, updating, deleting, and filtering entries. Test cases for thread-safety and eviction strategies are also included.


## Summary

This cache implementation offers a powerful solution for efficient data caching in Python projects. Leveraging the LRU eviction strategy and thread-safety mechanisms, it ensures that frequently accessed data is readily available, leading to improved performance. The detailed unit tests guarantee the reliability of the cache operations and behavior.
