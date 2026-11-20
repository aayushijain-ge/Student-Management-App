# Day 4: Database, Performance and Background Processing

## About this document

This document explains the work done and topics that covered and  what it is, which problem it solves, how it works, and how it was used in the Student Management App.

**Topics covered**

1. SQL vs NoSQL databases
2. Schema design basics
3. CRUD operations
4. Indexing and query optimization
5. Pagination and filtering
6. Caching fundamentals (Redis concept)
7. Background jobs and async tasks

**What was built:** the FastAPI backend was moved from an in-memory list to a SQLite database using SQLAlchemy, and pagination, filtering, caching and a Celery and Redis email job were added.

---

## 1. SQL vs NoSQL Databases

### Definition

A **database** is an organized store of data that survives after a program stops.

- **SQL (relational) databases** store data in tables with rows and columns, and use the SQL language to read and write. Examples: SQLite, PostgreSQL, MySQL.
- **NoSQL databases** store data in other shapes, such as documents (MongoDB), key-value pairs (Redis), columns or graphs. They usually do not require a fixed structure.

### Problem it solves

Storing data in a Python list works only while the program runs. When the server restarts, everything is lost. A database gives permanent storage, safe concurrent access and fast searching.

The next question is which kind of database to choose, because each solves a different problem.

### Comparison

| | SQL | NoSQL |
|---|---|---|
| Structure | Fixed columns and types | Flexible, can change per record |
| Relationships | Strong, through joins and foreign keys | Weaker, data is often duplicated instead |
| Consistency | Strong guarantees (ACID transactions) | Often relaxed in exchange for speed and scale |
| Scaling | Usually vertical first (bigger machine) | Designed for horizontal scaling (more machines) |
| Best for | Structured data: students, orders, payments | Changing data shapes, caching, huge volumes |

**ACID** means a transaction is Atomic (all or nothing), Consistent (rules always hold), Isolated (transactions do not disturb each other) and Durable (saved data stays saved).

### Choice in this project

SQL, using **SQLite**. Student records have a fixed, known structure, so a table fits naturally. SQLite is a complete SQL database stored in a single file, so no server needs to be installed. Moving to PostgreSQL later only requires changing the connection URL, because SQLAlchemy hides the differences.

NoSQL appears in the project too: **Redis** is a key-value store, used as the message queue for background jobs.

---

## 2. Schema Design Basics

### Definition

A **schema** is the blueprint of a database: which tables exist, which columns each has, the type of each column, and the rules (constraints) that data must follow.

### Problem it solves

Without a planned structure, data becomes inconsistent: one student has an age, another has the text "twenty", another has none. Searching and validating becomes unreliable. A schema forces every row to follow the same rules.

### Key ideas

| Term | Meaning |
|---|---|
| **Table** | A collection of rows about one kind of thing (students) |
| **Column** | One attribute, with a fixed type (age is an integer) |
| **Primary key** | A column that uniquely identifies each row (`id`) |
| **Unique constraint** | No two rows may have the same value (`username`) |
| **Not null** | The column must have a value |
| **Foreign key** | A column that points to a row in another table (not needed yet in this project) |
| **Normalization** | Splitting data into tables so each fact is stored once |

### Schema used in this project

**students**

| Column | Type | Notes |
|---|---|---|
| id | INTEGER | Primary key |
| name | VARCHAR(50) | Indexed |
| age | INTEGER | |
| course | VARCHAR(50) | Indexed |

**users**

| Column | Type | Notes |
|---|---|---|
| id | INTEGER | Primary key |
| username | VARCHAR(20) | Unique, indexed |
| email | VARCHAR(255) | Unique, indexed |
| hashed_password | VARCHAR(255) | Hash, never the real password |

### Design decisions

- Passwords are **hashed**, not stored as text. A hash is a one-way transformation, so even if the database leaks, the original passwords cannot be read back.
- `username` and `email` are **unique at the database level**, so duplicates are rejected even if the application code has a bug.

### Models vs schemas

Two different things share the word "schema" in this project:

- **Models** (`models/`, SQLAlchemy) describe the database tables.
- **Schemas** (`schemas/`, Pydantic) describe what the API accepts and returns.

They are separate so the API can hide sensitive columns (like `hashed_password`) and the two can change independently.

### ORM

An **ORM** (Object-Relational Mapper) lets you work with Python classes instead of writing SQL. A class `Student` with `__tablename__ = "students"` becomes the `students` table. `Base.metadata.create_all()` creates the tables on startup.

---

## 3. CRUD Operations

### Definition

CRUD stands for **Create, Read, Update, Delete**, the four basic operations on stored data.

| Operation | SQL | HTTP method | Endpoint |
|---|---|---|---|
| Create | INSERT | POST | `/students` |
| Read | SELECT | GET | `/students`, `/students/{id}` |
| Update | UPDATE | PUT | `/students/{id}` |
| Delete | DELETE | DELETE | `/students/{id}` |

### Problem it solves

Almost every application needs to store, show, change and remove records. CRUD gives a standard, predictable way to expose these operations through an API (REST).

### How it works with a database

Each request opens a **session**, which is one conversation with the database. The session is closed when the request ends.

1. `db.add(obj)` marks a new object to be saved.
2. `db.commit()` writes the changes permanently. Until commit, nothing is saved.
3. `db.refresh(obj)` reloads the object so values the database generated (like `id`) are available.
4. If the record does not exist, the API returns **404**.

The code is split in layers: the **router** handles HTTP and status codes, the **service** holds the logic and database calls, the **model** defines the table. A change in one layer, such as replacing the database, does not force changes in the others.




---

## 4. Indexing and Query Optimization

### Definition

An **index** is an extra data structure that the database keeps beside a table so it can find rows without reading the whole table. It works like the index at the back of a book.

### Problem it solves

Without an index, a query such as `WHERE course = 'Python'` must check every row. This is a **full table scan**. The time grows with the number of rows: 100 rows is instant, 10 million rows is slow.

### How it works: the B-Tree

Most databases build indexes as a **B-Tree**, a balanced tree with sorted keys.

- Each node holds many keys in sorted order.
- Searching goes from the root down, choosing a branch at each level, like binary search.
- When a node becomes full it **splits**, and the middle key moves up. The tree grows upward, so all leaves stay at the same depth.
- Because a node holds many keys, the tree is very shallow: about 4 levels are enough for 100 million rows.

| | Cost |
|---|---|
| Full scan | Grows with N (O(n)) |
| B-Tree search | Grows with log N (O(log n)) |

### Types of index

| Type | Purpose | Used here |
|---|---|---|
| Primary key | Identifies rows, automatic index | `id` |
| Normal | Speeds up search | `name`, `course` |
| Unique | Speeds up search and blocks duplicates | `username`, `email` |
| Composite | Several columns together; only works from the leftmost column | Optional |

### Where indexes are used in this project

- `users.username`: looked up on every login and every token check.
- `students.course`: used by the `?course=` filter.
- Primary keys: used when getting, updating and deleting by id.

### When an index does not help

| Query | Reason |
|---|---|
| `LIKE '%aay%'` | The tree is sorted from the first letter, so a match in the middle cannot be located |
| `lower(name) = 'x'` | The function changes the value, so the sorted order no longer applies |
| Column without an index (`age`) | The database falls back to a scan |
| Composite index used without its first column | Leftmost column rule |

### Trade-off

Indexes make **reads faster** but **writes slower**, because every insert, update and delete must also update the index. They also use disk space. Index only the columns you frequently search, filter or sort by.

### Query optimization

**Query optimization** means making queries do less work. The method is:

1. Find the slow query.
2. Look at its plan with `EXPLAIN QUERY PLAN`.
3. If a large table shows `SCAN`, add an index on the filtered column.
4. Check the plan and time again.

```sql
EXPLAIN QUERY PLAN SELECT * FROM students WHERE course = 'Python';
-- SEARCH students USING INDEX ix_students_course   (index used)

EXPLAIN QUERY PLAN SELECT * FROM students WHERE age = 22;
-- SCAN students                                     (no index)
```

Other optimization habits used here: filtering and counting in SQL instead of Python loops, never loading all rows, and limiting page size.

---

## 5. Pagination and Filtering

### Definition

- **Filtering** returns only the rows that match a condition (the SQL `WHERE`).
- **Pagination** returns the result in small pages instead of all at once (`LIMIT` and `OFFSET`).

### Problem it solves

`GET /students` used to return every row. With 100,000 students this fills server memory, makes a huge response, slows the network and freezes the user interface. Users also rarely need everything: they need a page, or the rows matching a search.

### How it works

```
GET /students?skip=20&limit=10&course=Python&search=aay
```

| Parameter | Rule | Meaning |
|---|---|---|
| `skip` | 0 or more | Rows to skip. `skip = (page - 1) * limit` |
| `limit` | 1 to 100, default 10 | Page size, capped so nobody can request a million rows |
| `course` | optional, exact match | Uses the course index |
| `search` | optional, contains, ignores case | Matches the student name |

All filters are optional, and only the supplied ones are applied.

**Processing order matters:**

1. **Filter**: apply `WHERE`.
2. **Count**: count the filtered rows to get `total`.
3. **Sort**: `ORDER BY id`, so pages are stable and do not repeat or miss rows.
4. **Paginate**: `OFFSET skip LIMIT limit`.

Paginating before filtering would give wrong pages and a wrong total.

### Response

```json
{
  "total": 23,
  "skip": 0,
  "limit": 10,
  "items": [ { "id": 1, "name": "Aayushi", "age": 22, "course": "Python" } ]
}
```

`total` lets the frontend compute the number of pages: `ceil(total / limit)`.

### Validation

Values such as `limit=0`, `limit=500` or `skip=-1` are rejected with **422** before any database work, using FastAPI `Query(...)` rules.

### Offset vs cursor pagination

| | Offset (used here) | Cursor |
|---|---|---|
| Style | `skip` and `limit` | `WHERE id > last_id LIMIT n` |
| Jump to page 5 | Yes | No, only next or previous |
| Very large tables | Slower, skipped rows are still read | Fast, uses the index |
| Data changing while paging | Rows can repeat or be missed | Stable |
| Typical use | Admin tables | Infinite scroll, feeds |

Offset pagination is simple and enough for this project.

### Filtering and indexes

The `course` filter is an exact match, so it uses the index. The `search` filter uses `%text%`, which cannot use a B-Tree index and scans the table. That is acceptable for small and medium data; at large scale, full-text search is used instead.

---

## 6. Caching Fundamentals (Redis Concept)

### Definition

A **cache** is a fast, temporary storage that keeps the result of an expensive operation so the same request can be answered without repeating the work.

### Problem it solves

If many users request the same list, the database runs the same query and count again and again, even though the data has not changed. This wastes time and database capacity.

### Cache-aside pattern (used here)

```
GET request
  → build a key from the query parameters
  → key found and not expired  → HIT: return the stored result
  → otherwise                  → MISS: query the database, store the result, return it

POST / PUT / DELETE
  → change the database
  → clear the cached entries
```

### Key concepts

| Concept | Meaning | In this project |
|---|---|---|
| **Key** | Identifies one cached result | `students:search=None:course=Python:skip=0:limit=10` |
| **HIT / MISS** | Found in cache / not found | Printed in the server terminal |
| **TTL** | Time To Live, how long an entry stays valid | 60 seconds |
| **Invalidation** | Removing cached data when the source data changes | `cache.clear_prefix("students:")` after create, update, delete |
| **Stale data** | A cached value that no longer matches the database | Limited by TTL and invalidation |

The key must contain every parameter that changes the result. Otherwise a request for Java students could receive the cached list of Python students.

Cache invalidation is considered one of the hardest problems in software, because forgetting one case shows users wrong data.

### What to cache and what not to

| Cache | Do not cache |
|---|---|
| Lists read often | Login, registration, token verification (security risk) |
| Data that changes rarely | Data that changes every second |
| Expensive queries (joins, counts) | Writes (POST, PUT, DELETE) |

### Implementation notes

The cache is a Python dictionary mapping `key → (expiry time, value)`. Plain dictionaries are cached instead of database objects, because database objects belong to a session that closes after the request.

### Redis

**Redis** is an in-memory key-value database (a NoSQL store) commonly used as a cache.

| | Dictionary cache (used here) | Redis |
|---|---|---|
| Location | Inside the server process | Separate server |
| Survives a restart | No | Yes, if configured |
| Shared by several workers or servers | No, each has its own | Yes |
| Built-in expiry | Written manually | Yes |

The logic (key, TTL, invalidate on write) is the same. In production, only `cache.py` would change to talk to Redis.

---

## 7. Background Jobs and Async Tasks

### Definition

A **background job** is work that runs outside the request-response cycle, so the user gets a reply without waiting for it to finish.

### Problem it solves

When a user registers, we want to send a welcome email. Sending email can take seconds. If it runs inside the request, the user waits for something they do not need to wait for, and if the mail server is slow or down, the registration itself seems to fail.

```
Inside the request:   save user → send email (3 s) → respond      user waits
Background job:       save user → queue job → respond             instant
                                       └→ worker sends the email later
```

**Rule:** if the response needs the result, do the work in the request. If it is a side effect (email, logging, report, image processing), do it in the background.

### approache

| | FastAPI BackgroundTasks | Task queue (Celery + Redis) |
|---|---|---|
| How | Runs after the response, in the same process | A separate worker process takes jobs from a queue |
| Setup | None | Redis and a worker |
| Server crash | Job is lost | Job stays in the queue |
| Retries | No | Yes |
| Scheduling | No | Yes |
| Heavy work | Competes with the API for CPU | Runs separately |
| Use for | Small, non-critical side effects | Important, heavy or scheduled jobs |

This project uses Celery and Redis.

### Components

| Component | Role |
|---|---|
| **Producer** | The FastAPI app. It calls `send_welcome_email.delay(...)`, which only puts a message in the queue |
| **Broker** | Redis. It holds the waiting jobs |
| **Worker** | A Celery process. It takes jobs from the broker and runs them |
| **Task** | The function to run: `send_welcome_email` |

### Flow

```
POST /auth/register
  → user saved in the database
  → job added to Redis (about 1 ms)
  → API returns 201 immediately

Celery worker
  → takes the job from Redis
  → sends the email over SMTP
  → on failure, retries up to 3 times with increasing delay
```

If the worker is stopped, jobs wait in Redis and are processed when it starts again.

### Design decisions

- The task is a normal `def`, because SMTP is blocking code. It runs in the worker process, so the API is never blocked.
- Retries use `autoretry_for`, `retry_backoff` and `max_retries=3`.
- If Redis is down, registration still succeeds and the error is logged, because the email is not essential.
- SMTP credentials come from the `.env` file, never from the code.

### Sync, async and blocking

- **Blocking** code makes the program wait (`time.sleep`, SMTP, normal database drivers).
- **Non-blocking** code lets other work run while waiting (`await asyncio.sleep`).
- FastAPI runs `async def` routes on the event loop, and plain `def` routes in a thread pool. Blocking code inside `async def` freezes the whole server, so blocking work goes either in a plain `def` or in a separate worker.

### Cautions

1. A failure in a background job does not reach the user, because the response is already sent. The task must log its own errors.
2. Jobs may run more than once (retries), so they should be safe to repeat.
3. Do not pass the request's database session to a job. It is closed after the response; open a new one inside the job.

---
