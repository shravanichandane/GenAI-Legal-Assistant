"""
Module 0.3 — Database & PostgreSQL Tests
==========================================

These tests verify that your database schema, relationships, and CRUD
operations all work correctly.

Run with:
    python -m pytest tests/test_database.py -v

Key Concepts Tested:
    - Table creation (DDL)
    - Primary Keys (uniqueness)
    - Foreign Keys (referential integrity)
    - Relationships (ORM navigation)
    - CRUD operations (Create, Read, Update, Delete)
    - Indexes (query performance)
    - Session lifecycle

Interview Tip:
    Q: "How do you test database code without a real database?"
    A: I use an in-memory or file-based SQLite database for unit tests.
       SQLAlchemy's ORM abstraction means the same Python code works
       against both SQLite (tests) and PostgreSQL (production).
       For integration tests, I would use a Docker-based PostgreSQL
       with testcontainers or a CI service like GitHub Actions.
"""

import pytest
from datetime import datetime
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker

import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from backend.database import Base
from backend.models import Document, Clause
from backend.auth import User

# ---------------------------------------------------------------------------
# Test Database Setup
# ---------------------------------------------------------------------------

TEST_DATABASE_URL = "sqlite:///./test_database.db"
test_engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestSession = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(autouse=True)
def setup_database():
    """Create fresh tables before each test, drop after."""
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture
def db():
    """Provide a clean database session for each test."""
    session = TestSession()
    try:
        yield session
    finally:
        session.close()


# ---------------------------------------------------------------------------
# HELPERS
# ---------------------------------------------------------------------------

def create_test_user(db, email="test@example.com") -> User:
    """Create and return a test user."""
    user = User(
        email=email,
        hashed_password="fakehash123",
        full_name="Test User",
        is_active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def create_test_document(db, user: User, filename="contract.pdf") -> Document:
    """Create and return a test document linked to a user."""
    doc = Document(
        filename=filename,
        content="The Contractor shall indemnify and hold harmless the Client.",
        user_id=user.id,
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc


def create_test_clause(db, doc: Document, clause_type="INDEMNITY") -> Clause:
    """Create and return a test clause linked to a document."""
    clause = Clause(
        document_id=doc.id,
        clause_text="The Contractor shall indemnify the Client.",
        summary="Indemnification obligation.",
        clause_type=clause_type,
        risk_score=8.5,
        risk_level="HIGH",
    )
    db.add(clause)
    db.commit()
    db.refresh(clause)
    return clause


# ═══════════════════════════════════════════════════════════════════════════
# TEST SUITE 1: Table Creation (DDL)
# ═══════════════════════════════════════════════════════════════════════════

class TestTableCreation:
    """Verify that all tables are created with the correct columns.

    Concept: DDL (Data Definition Language)
    When SQLAlchemy calls Base.metadata.create_all(), it generates
    CREATE TABLE statements from your Python model classes.
    """

    def test_users_table_exists(self):
        """The 'users' table should be created."""
        inspector = inspect(test_engine)
        tables = inspector.get_table_names()
        assert "users" in tables

    def test_documents_table_exists(self):
        """The 'documents' table should be created."""
        inspector = inspect(test_engine)
        tables = inspector.get_table_names()
        assert "documents" in tables

    def test_clauses_table_exists(self):
        """The 'clauses' table should be created."""
        inspector = inspect(test_engine)
        tables = inspector.get_table_names()
        assert "clauses" in tables

    def test_users_table_has_correct_columns(self):
        """Users table should have: id, email, hashed_password, etc."""
        inspector = inspect(test_engine)
        columns = {col["name"] for col in inspector.get_columns("users")}
        expected = {"id", "email", "hashed_password", "full_name", "is_active", "created_at"}
        assert expected.issubset(columns), f"Missing columns: {expected - columns}"

    def test_documents_table_has_correct_columns(self):
        """Documents table should have: id, filename, content, user_id, etc."""
        inspector = inspect(test_engine)
        columns = {col["name"] for col in inspector.get_columns("documents")}
        expected = {"id", "filename", "content", "upload_date", "user_id"}
        assert expected.issubset(columns), f"Missing columns: {expected - columns}"

    def test_clauses_table_has_correct_columns(self):
        """Clauses table should have: id, document_id, clause_text, etc."""
        inspector = inspect(test_engine)
        columns = {col["name"] for col in inspector.get_columns("clauses")}
        expected = {"id", "document_id", "clause_text", "summary",
                    "risk_score", "risk_level", "clause_type", "last_updated"}
        assert expected.issubset(columns), f"Missing columns: {expected - columns}"


# ═══════════════════════════════════════════════════════════════════════════
# TEST SUITE 2: Primary Keys (Uniqueness)
# ═══════════════════════════════════════════════════════════════════════════

class TestPrimaryKeys:
    """Verify that primary keys auto-increment and are unique.

    Concept: Primary Key
    A PK uniquely identifies each row.  SQLAlchemy's Integer PK
    auto-increments by default in SQLite and PostgreSQL.
    """

    def test_user_id_auto_increments(self, db):
        """Each user should get a unique, incrementing ID."""
        u1 = create_test_user(db, "user1@test.com")
        u2 = create_test_user(db, "user2@test.com")
        assert u1.id is not None
        assert u2.id is not None
        assert u1.id != u2.id
        assert u2.id > u1.id

    def test_document_id_auto_increments(self, db):
        """Each document should get a unique ID."""
        user = create_test_user(db)
        d1 = create_test_document(db, user, "doc1.pdf")
        d2 = create_test_document(db, user, "doc2.pdf")
        assert d1.id != d2.id

    def test_user_email_must_be_unique(self, db):
        """Inserting two users with the same email should fail.

        This tests the `unique=True` constraint on the email column.
        """
        create_test_user(db, "same@test.com")
        with pytest.raises(Exception):
            create_test_user(db, "same@test.com")


# ═══════════════════════════════════════════════════════════════════════════
# TEST SUITE 3: Foreign Keys (Referential Integrity)
# ═══════════════════════════════════════════════════════════════════════════

class TestForeignKeys:
    """Verify that foreign keys enforce relationships.

    Concept: Foreign Key
    A FK column references another table's PK.  It ensures that
    you can't create a clause for a document that doesn't exist.
    """

    def test_document_references_user(self, db):
        """Document.user_id should reference an existing user."""
        user = create_test_user(db)
        doc = create_test_document(db, user)
        assert doc.user_id == user.id

    def test_clause_references_document(self, db):
        """Clause.document_id should reference an existing document."""
        user = create_test_user(db)
        doc = create_test_document(db, user)
        clause = create_test_clause(db, doc)
        assert clause.document_id == doc.id

    def test_document_can_have_null_user(self, db):
        """Documents with nullable=True should work without a user.

        This is useful for documents uploaded before auth was implemented.
        """
        doc = Document(
            filename="orphan.pdf",
            content="No owner assigned.",
            user_id=None,
        )
        db.add(doc)
        db.commit()
        db.refresh(doc)
        assert doc.user_id is None
        assert doc.id is not None


# ═══════════════════════════════════════════════════════════════════════════
# TEST SUITE 4: Relationships (ORM Navigation)
# ═══════════════════════════════════════════════════════════════════════════

class TestRelationships:
    """Verify that SQLAlchemy relationship() allows navigation.

    Concept: ORM Relationships
    relationship() creates a Python attribute that auto-fetches
    related objects.  It doesn't create a database column.
    """

    def test_user_has_documents(self, db):
        """user.documents should return all documents owned by that user."""
        user = create_test_user(db)
        create_test_document(db, user, "doc1.pdf")
        create_test_document(db, user, "doc2.pdf")

        # Refresh to load relationships
        db.refresh(user)
        assert len(user.documents) == 2
        assert user.documents[0].filename == "doc1.pdf"

    def test_document_has_clauses(self, db):
        """doc.clauses should return all clauses in that document."""
        user = create_test_user(db)
        doc = create_test_document(db, user)
        create_test_clause(db, doc, "INDEMNITY")
        create_test_clause(db, doc, "PAYMENT")

        db.refresh(doc)
        assert len(doc.clauses) == 2
        types = {c.clause_type for c in doc.clauses}
        assert types == {"INDEMNITY", "PAYMENT"}

    def test_document_has_owner(self, db):
        """doc.owner should navigate back to the user."""
        user = create_test_user(db)
        doc = create_test_document(db, user)

        db.refresh(doc)
        assert doc.owner is not None
        assert doc.owner.email == "test@example.com"

    def test_clause_has_document(self, db):
        """clause.document should navigate back to the document."""
        user = create_test_user(db)
        doc = create_test_document(db, user)
        clause = create_test_clause(db, doc)

        db.refresh(clause)
        assert clause.document is not None
        assert clause.document.filename == "contract.pdf"

    def test_full_chain_user_to_clause(self, db):
        """Navigate the full chain: User → Document → Clause."""
        user = create_test_user(db)
        doc = create_test_document(db, user)
        create_test_clause(db, doc, "LIABILITY")

        db.refresh(user)
        first_doc = user.documents[0]
        first_clause = first_doc.clauses[0]
        assert first_clause.clause_type == "LIABILITY"
        assert first_clause.document.owner.email == "test@example.com"


# ═══════════════════════════════════════════════════════════════════════════
# TEST SUITE 5: CRUD Operations
# ═══════════════════════════════════════════════════════════════════════════

class TestCRUD:
    """Verify Create, Read, Update, Delete operations.

    These are the four fundamental database operations.
    Every API endpoint maps to one of these.
    """

    def test_create_and_read_user(self, db):
        """CREATE a user, then READ it back."""
        user = create_test_user(db)
        fetched = db.query(User).filter(User.email == "test@example.com").first()
        assert fetched is not None
        assert fetched.id == user.id

    def test_create_and_read_clause(self, db):
        """CREATE a clause, then READ it back."""
        user = create_test_user(db)
        doc = create_test_document(db, user)
        clause = create_test_clause(db, doc)

        fetched = db.query(Clause).filter(Clause.id == clause.id).first()
        assert fetched.clause_type == "INDEMNITY"
        assert fetched.risk_score == 8.5

    def test_update_clause_risk(self, db):
        """UPDATE a clause's risk score."""
        user = create_test_user(db)
        doc = create_test_document(db, user)
        clause = create_test_clause(db, doc)

        # Update
        clause.risk_score = 3.0
        clause.risk_level = "LOW"
        db.commit()
        db.refresh(clause)

        assert clause.risk_score == 3.0
        assert clause.risk_level == "LOW"

    def test_delete_clause(self, db):
        """DELETE a clause from the database."""
        user = create_test_user(db)
        doc = create_test_document(db, user)
        clause = create_test_clause(db, doc)
        clause_id = clause.id

        db.delete(clause)
        db.commit()

        deleted = db.query(Clause).filter(Clause.id == clause_id).first()
        assert deleted is None

    def test_query_clauses_by_risk_level(self, db):
        """Filter clauses by risk_level (common query in your app)."""
        user = create_test_user(db)
        doc = create_test_document(db, user)

        # Create mixed risk clauses
        c1 = Clause(document_id=doc.id, clause_text="Safe clause", risk_level="LOW", risk_score=1.0)
        c2 = Clause(document_id=doc.id, clause_text="Dangerous clause", risk_level="HIGH", risk_score=9.0)
        c3 = Clause(document_id=doc.id, clause_text="Risky clause", risk_level="HIGH", risk_score=8.0)
        db.add_all([c1, c2, c3])
        db.commit()

        high_risk = db.query(Clause).filter(Clause.risk_level == "HIGH").all()
        assert len(high_risk) == 2

    def test_query_clauses_by_type(self, db):
        """Filter clauses by clause_type."""
        user = create_test_user(db)
        doc = create_test_document(db, user)

        c1 = Clause(document_id=doc.id, clause_text="A", clause_type="INDEMNITY")
        c2 = Clause(document_id=doc.id, clause_text="B", clause_type="PAYMENT")
        c3 = Clause(document_id=doc.id, clause_text="C", clause_type="INDEMNITY")
        db.add_all([c1, c2, c3])
        db.commit()

        indemnity = db.query(Clause).filter(Clause.clause_type == "INDEMNITY").all()
        assert len(indemnity) == 2

    def test_count_documents_per_user(self, db):
        """Aggregation: count how many documents a user has."""
        user = create_test_user(db)
        create_test_document(db, user, "doc1.pdf")
        create_test_document(db, user, "doc2.pdf")
        create_test_document(db, user, "doc3.pdf")

        count = db.query(Document).filter(Document.user_id == user.id).count()
        assert count == 3


# ═══════════════════════════════════════════════════════════════════════════
# TEST SUITE 6: Schema Inspection (Indexes)
# ═══════════════════════════════════════════════════════════════════════════

class TestIndexes:
    """Verify that indexes exist on frequently queried columns.

    Concept: Indexes
    An index is a B-tree that speeds up WHERE, ORDER BY, and JOIN.
    Without it, the DB does a full table scan (O(n)).
    With it, lookups are O(log n).
    """

    def test_users_email_is_indexed(self):
        """Email should be indexed for fast login lookups."""
        inspector = inspect(test_engine)
        indexes = inspector.get_indexes("users")
        indexed_columns = {col for idx in indexes for col in idx["column_names"]}
        assert "email" in indexed_columns

    def test_documents_filename_is_indexed(self):
        """Filename should be indexed for search."""
        inspector = inspect(test_engine)
        indexes = inspector.get_indexes("documents")
        indexed_columns = {col for idx in indexes for col in idx["column_names"]}
        assert "filename" in indexed_columns
