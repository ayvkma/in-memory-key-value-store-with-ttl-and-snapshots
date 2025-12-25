# `In-memory key-value store`

## What is this project?
- This project demonstrates an In Memory Key-Value Store with SET/GET/DELETE/EXPIRE commands.
- Supports TTL-based expiration and snapshot-based persistence.

## Features
- In-memory storage for fast read/write access
- TTL-based key expiration
- Background cleanup of expired keys
- Snapshot-based persistence with atomic file replacement
- Load-on-start recovery from the latest snapshot

## What problem it solves?
- Provides fast, in-memory access to frequently used data with time-based expiration, while supporting basic durability via snapshots.

## Limitations

This project intentionally trades off certain production-level guarantees in order to
focus on core concepts such as in-memory state management, TTL semantics, and snapshot-based persistence.

- No locking: concurrent access between the CLI thread and cleanup thread may cause race conditions.
- Snapshot frequency is tied to the cleanup interval, so recent writes may be lost on crash.
- No write-ahead log (WAL), durability is snapshot-based only.
- Snapshot file grows over time, no compaction or rotation is implemented.
- System clock changes (clock skew) are not handled.
- Single-process design, multiple instances sharing the same snapshot file are unsupported.

These limitations are intentional and documented as future improvement areas.

## How to run it ?

### `Requirements`
- Python version >= 3.12.0

### Clone the repo: 

1.
    ```
    git clone https://github.com/ayvkma/in-memory-key-value-store-with-ttl-and-snapshots.git
    ```
2.  ```python
    python main.py
    ```
    
## Key Learnings
- In-memory state management
- TTL and time-based data expiration
- Background task scheduling
- Snapshot-based persistence
- Designing systems with explicit trade-offs


