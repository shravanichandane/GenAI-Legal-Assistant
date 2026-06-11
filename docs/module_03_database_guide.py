"""
===========================================================================
MODULE 0.3 — PostgreSQL & Databases Reference Guide
===========================================================================

This file explains every database concept used in your existing backend,
using YOUR actual tables as examples.  Read top to bottom.

After reading this, you should be able to answer:

1. What problem does a database solve?
   → It persists data beyond the lifetime of your Python process.
     Without a database, every uploaded contract would vanish when the
     server restarts.

2. Why PostgreSQL over SQLite?
   → SQLite writes to a single file on disk. It cannot handle concurrent
     writes (multiple users uploading at the same time) and fails on
     read-only filesystems (Streamlit Cloud, Docker).
     PostgreSQL runs as a separate server, handles thousands of
     concurrent connections, and provides advanced features like JSONB,
     full-text search, and row-level locking.

3. How does it work internally?
   → Your Python code talks to SQLAlchemy (the ORM), which translates
     Python classes into SQL statements.  SQLAlchemy sends those SQL
     statements to the database engine (SQLite locally, PostgreSQL in
     production).  The database engine stores data on disk in B-tree
     indexed files.

4. What alternatives exist?
   → MongoDB (document store), DynamoDB (key-value), Redis (in-memory),
     MySQL, CockroachDB, Supabase (Postgres-as-a-Service).

5. What metrics evaluate it?
   → Query latency (ms), throughput (queries/sec), index hit ratio,
     connection pool utilisation.

6. How would I explain it in an interview?
   → "I designed a relational schema with Users, Documents, and Clauses
      tables connected by foreign keys.  SQLAlchemy ORM handles the
      object-relational mapping, and I use dependency injection to
      manage database session lifecycle.  In production, I use Neon
      PostgreSQL with pool_pre_ping to handle connection drops."

===========================================================================
"""


# ═══════════════════════════════════════════════════════════════════════════
# CONCEPT 1: TABLES, ROWS, AND COLUMNS
# ═══════════════════════════════════════════════════════════════════════════
#
# A table is like a spreadsheet:
#   - Each COLUMN is a field (id, filename, risk_score)
#   - Each ROW is one record (one document, one clause, one user)
#
# YOUR TABLES:
#
#   ┌──────────────────────────────────────────────────────────────────┐
#   │                         users                                    │
#   ├──────────┬──────────────────┬─────────┬──────────┬──────────────┤
#   │ id (PK)  │ email (UNIQUE)   │ full_name│ is_active│ created_at   │
#   ├──────────┼──────────────────┼─────────┼──────────┼──────────────┤
#   │ 1        │ alice@firm.com   │ Alice   │ True     │ 2026-06-01   │
#   │ 2        │ bob@firm.com     │ Bob     │ True     │ 2026-06-01   │
#   └──────────┴──────────────────┴─────────┴──────────┴──────────────┘
#
#   ┌──────────────────────────────────────────────────────────────────┐
#   │                       documents                                  │
#   ├──────────┬───────────┬──────────────┬────────────────────────────┤
#   │ id (PK)  │ filename  │ user_id (FK) │ upload_date                │
#   ├──────────┼───────────┼──────────────┼────────────────────────────┤
#   │ 1        │ nda.pdf   │ 1            │ 2026-06-01  (← Alice)     │
#   │ 2        │ msa.docx  │ 2            │ 2026-06-01  (← Bob)       │
#   └──────────┴───────────┴──────────────┴────────────────────────────┘
#
#   ┌──────────────────────────────────────────────────────────────────┐
#   │                        clauses                                   │
#   ├──────────┬────────────────┬────────────┬────────────┬───────────┤
#   │ id (PK)  │ document_id(FK)│ clause_type│ risk_score │ risk_level│
#   ├──────────┼────────────────┼────────────┼────────────┼───────────┤
#   │ 1        │ 1              │ INDEMNITY  │ 8.5        │ HIGH      │
#   │ 2        │ 1              │ PAYMENT    │ 2.0        │ LOW       │
#   │ 3        │ 2              │ LIABILITY  │ 9.1        │ HIGH      │
#   └──────────┴────────────────┴────────────┴────────────┴───────────┘
#


# ═══════════════════════════════════════════════════════════════════════════
# CONCEPT 2: PRIMARY KEYS
# ═══════════════════════════════════════════════════════════════════════════
#
# A Primary Key (PK) is the UNIQUE IDENTIFIER for each row.
# No two rows can have the same PK.  It's usually an auto-incrementing
# integer called `id`.
#
# YOUR CODE:
#   id = Column(Integer, primary_key=True, index=True)
#
# What `primary_key=True` does:
#   1. Guarantees uniqueness (no duplicates)
#   2. Creates a B-tree index automatically (fast lookups)
#   3. Cannot be NULL
#
# Interview Tip:
#   Q: "Why not use email as the primary key for users?"
#   A: Emails can change.  Using a synthetic integer PK (surrogate key)
#      means all foreign key references remain valid even if the user
#      updates their email.  Also, integer comparisons are faster than
#      string comparisons in JOINs.
#


# ═══════════════════════════════════════════════════════════════════════════
# CONCEPT 3: FOREIGN KEYS (Relationships Between Tables)
# ═══════════════════════════════════════════════════════════════════════════
#
# A Foreign Key (FK) is a column that POINTS TO another table's PK.
# It creates a relationship between tables.
#
# YOUR CODE has two foreign keys:
#
#   1. documents.user_id → users.id
#      "Every document belongs to one user"
#
#   2. clauses.document_id → documents.id
#      "Every clause belongs to one document"
#
# This creates a chain:
#   User ──(has many)──▶ Documents ──(has many)──▶ Clauses
#
# In SQL terms:
#   user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
#
# The `nullable=True` means a document CAN exist without an owner.
# The `ForeignKey("users.id")` means the database will REJECT any
# document with a user_id that doesn't exist in the users table.
# This is called REFERENTIAL INTEGRITY.
#
# Interview Tip:
#   Q: "What happens if you delete a user who has documents?"
#   A: By default, the database will REJECT the delete because the
#      documents still reference that user.  You can change this with
#      CASCADE (delete the documents too) or SET NULL (set user_id
#      to NULL).  In a legal system, you'd probably want SET NULL
#      to preserve document history.
#


# ═══════════════════════════════════════════════════════════════════════════
# CONCEPT 4: INDEXES (Speed Up Queries)
# ═══════════════════════════════════════════════════════════════════════════
#
# Without an index, the database scans EVERY ROW to find matches.
# With 100,000 clauses, that's slow.
#
# An index is a separate data structure (B-tree) that allows O(log n)
# lookups instead of O(n).
#
# YOUR CODE creates indexes on:
#   - users.id          (automatic, it's a PK)
#   - users.email       (index=True — for login lookups)
#   - documents.id      (automatic, PK)
#   - documents.filename (index=True — for searching by name)
#   - clauses.id        (automatic, PK)
#
# MISSING indexes that would help your app:
#   - clauses.clause_type  (for filtering "show me all INDEMNITY clauses")
#   - clauses.risk_level   (for filtering "show me all HIGH risk clauses")
#   - clauses.document_id  (for the JOIN when fetching clauses for a doc)
#
# Interview Tip:
#   Q: "When should you NOT add an index?"
#   A: Every index speeds up reads but slows down writes (inserts/updates)
#      because the index must be updated too.  Don't index columns you
#      rarely filter or sort on.  Also, don't index boolean columns
#      (like is_active) — with only 2 values, the index doesn't help.
#


# ═══════════════════════════════════════════════════════════════════════════
# CONCEPT 5: RELATIONSHIPS (ORM Navigation)
# ═══════════════════════════════════════════════════════════════════════════
#
# SQLAlchemy `relationship()` is NOT a database column.
# It's a Python-level shortcut that lets you navigate between objects.
#
# YOUR CODE:
#
#   # In Document model:
#   clauses = relationship("Clause", back_populates="document")
#   owner = relationship("User", back_populates="documents")
#
#   # In Clause model:
#   document = relationship("Document", back_populates="clauses")
#
# This means you can write:
#   doc = db.query(Document).first()
#   for clause in doc.clauses:      # ← SQLAlchemy auto-fetches clauses
#       print(clause.risk_level)
#
#   user = doc.owner                # ← SQLAlchemy auto-fetches the user
#   print(user.email)
#
# Under the hood, SQLAlchemy generates a JOIN query:
#   SELECT * FROM clauses WHERE document_id = 1;
#
# Interview Tip:
#   Q: "What's the N+1 query problem?"
#   A: If you have 100 documents and call doc.clauses for each one,
#      SQLAlchemy fires 100 separate queries (1 for docs + 100 for clauses).
#      The fix: use `joinedload()` or `selectinload()` to fetch everything
#      in 1 or 2 queries:
#
#        from sqlalchemy.orm import joinedload
#        docs = db.query(Document).options(joinedload(Document.clauses)).all()
#


# ═══════════════════════════════════════════════════════════════════════════
# CONCEPT 6: SQLAlchemy ORM vs RAW SQL
# ═══════════════════════════════════════════════════════════════════════════
#
# The ORM maps Python classes to database tables.
# Here's the same query in both styles:
#
# RAW SQL:
#   SELECT * FROM clauses WHERE risk_level = 'HIGH' AND document_id = 1;
#
# SQLAlchemy ORM:
#   db.query(Clause).filter(
#       Clause.risk_level == "HIGH",
#       Clause.document_id == 1
#   ).all()
#
# The ORM gives you:
#   ✓ Python objects instead of raw tuples
#   ✓ Type safety (your IDE knows Clause.risk_score is a float)
#   ✓ Database portability (switch SQLite → PostgreSQL without rewriting)
#   ✓ Relationship navigation (doc.clauses)
#
# The ORM costs you:
#   ✗ Slight overhead for complex queries
#   ✗ Hidden queries (N+1 problem)
#   ✗ Learning curve
#
# Interview Tip:
#   Q: "When would you use raw SQL instead of the ORM?"
#   A: For complex aggregations (window functions, CTEs), bulk inserts
#      (INSERT INTO ... SELECT), or performance-critical queries where
#      you need full control over the execution plan.
#


# ═══════════════════════════════════════════════════════════════════════════
# CONCEPT 7: SESSION LIFECYCLE (get_db)
# ═══════════════════════════════════════════════════════════════════════════
#
# YOUR CODE (database.py):
#
#   def get_db():
#       db = SessionLocal()    # Open connection
#       try:
#           yield db           # Hand it to the route function
#       finally:
#           db.close()         # ALWAYS close, even if the route crashes
#
# This is a GENERATOR used as a FastAPI Dependency.
# The `yield` keyword pauses execution — the route function runs —
# then `finally` guarantees cleanup.
#
# Why is this important?
#   - Database connections are EXPENSIVE (each one holds a TCP socket).
#   - If you forget to close, you get "connection pool exhausted" errors.
#   - The try/finally pattern guarantees no connection leaks.
#
# Interview Tip:
#   Q: "What is pool_pre_ping and why did you add it?"
#   A: Serverless PostgreSQL (like Neon) aggressively closes idle
#      connections.  pool_pre_ping=True tells SQLAlchemy to send a
#      lightweight 'SELECT 1' before each query.  If the connection
#      is dead, it transparently creates a new one instead of crashing
#      with 'SSL connection has been closed unexpectedly'.
#


# ═══════════════════════════════════════════════════════════════════════════
# YOUR COMPLETE ENTITY-RELATIONSHIP DIAGRAM
# ═══════════════════════════════════════════════════════════════════════════
#
#   ┌──────────────┐         ┌──────────────┐         ┌──────────────┐
#   │    users     │         │  documents   │         │   clauses    │
#   ├──────────────┤         ├──────────────┤         ├──────────────┤
#   │ id      (PK) │◀───────│ user_id (FK) │         │ document_id  │
#   │ email (UQ)   │   1:N  │ id      (PK) │◀───────│   (FK)       │
#   │ hashed_pw    │         │ filename     │   1:N  │ id      (PK) │
#   │ full_name    │         │ content      │         │ clause_text  │
#   │ is_active    │         │ upload_date  │         │ summary      │
#   │ created_at   │         └──────────────┘         │ risk_score   │
#   └──────────────┘                                  │ risk_level   │
#                                                     │ clause_type  │
#                                                     │ last_updated │
#                                                     └──────────────┘
#
#   Relationships:
#     User  ──(1:N)──▶  Document  ──(1:N)──▶  Clause
#     "One user has many documents, each document has many clauses"
#
