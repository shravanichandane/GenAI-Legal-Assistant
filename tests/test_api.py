"""
Module 0.2 — FastAPI Tests
===========================

These tests verify that your existing backend API works correctly.
They use FastAPI's TestClient, which simulates HTTP requests without
needing a running server.

Run with:
    python -m pytest tests/test_api.py -v

Key Concepts Tested:
    - HTTP methods (GET, POST, PUT)
    - Status codes (200, 201, 400, 401, 404, 422)
    - Pydantic validation (invalid data → 422)
    - Dependency Injection (auth, database)
    - CORS headers

Interview Tip:
    Q: "How do you test APIs without a running server?"
    A: FastAPI's TestClient wraps Starlette's TestClient, which creates
       an in-process ASGI app.  Requests never hit the network — they go
       directly to your route functions.  This makes tests fast (~1ms each)
       and deterministic (no network flakiness).
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Import the app and database utilities
import sys
from pathlib import Path

# Ensure project root is on path
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from backend.main import app
from backend.database import Base, get_db

# ---------------------------------------------------------------------------
# Test Database Setup
# ---------------------------------------------------------------------------
# We use a file-based SQLite database for tests so that:
# 1. Tests don't pollute your real database
# 2. Each test run starts fresh
# 3. Tests are fast (no network I/O)

TEST_DATABASE_URL = "sqlite:///./test_legal.db"
test_engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


def override_get_db():
    """Dependency override: returns a test database session.

    This is Dependency Injection in action! We swap the real database
    for a test database WITHOUT changing any production code.
    """
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


# Override the dependency
app.dependency_overrides[get_db] = override_get_db

# Create the test client (uses Starlette's TestClient + httpx 0.27)
client = TestClient(app)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def setup_database():
    """Create fresh tables before each test, drop them after.

    This is called a 'fixture' — it runs setup/teardown around each test.
    The `autouse=True` means every test in this file uses it automatically.
    """
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


def register_and_login() -> str:
    """Helper: Create a test user and return a JWT token.

    This demonstrates the full auth flow:
    1. POST /api/auth/register → creates user in database
    2. POST /api/auth/login → returns JWT token
    3. All subsequent requests include: Authorization: Bearer <token>
    """
    # Register
    register_response = client.post("/api/auth/register", json={
        "email": "test@example.com",
        "password": "securepassword123",
        "full_name": "Test User"
    })
    assert register_response.status_code == 201, (
        f"Registration failed: {register_response.text}"
    )

    # Login
    login_response = client.post("/api/auth/login", json={
        "email": "test@example.com",
        "password": "securepassword123"
    })
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    assert token, "Login did not return a token"
    return token


# ---------------------------------------------------------------------------
# TEST SUITE 1: Health Check (GET)
# ---------------------------------------------------------------------------

class TestHealthEndpoint:
    """Tests for GET /health — the simplest possible endpoint."""

    def test_health_returns_200(self):
        """A GET request to /health should return 200 OK."""
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_returns_status_healthy(self):
        """The response body should contain status: healthy."""
        response = client.get("/health")
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data


# ---------------------------------------------------------------------------
# TEST SUITE 2: Authentication (POST)
# ---------------------------------------------------------------------------

class TestAuthEndpoints:
    """Tests for /api/auth/* endpoints.

    Concepts demonstrated:
    - POST with JSON body
    - Status code 201 (Created)
    - Status code 400 (Duplicate email)
    - Status code 401 (Wrong password)
    - JWT token flow
    """

    def test_register_creates_user(self):
        """POST /api/auth/register with valid data → 201 Created."""
        response = client.post("/api/auth/register", json={
            "email": "newuser@example.com",
            "password": "strongpassword",
            "full_name": "New User"
        })
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "newuser@example.com"
        assert "id" in data

    def test_register_duplicate_email_returns_400(self):
        """Registering the same email twice → 400 Bad Request.

        This tests your uniqueness constraint on the email column.
        """
        payload = {
            "email": "duplicate@example.com",
            "password": "password123",
            "full_name": "User"
        }
        client.post("/api/auth/register", json=payload)
        response = client.post("/api/auth/register", json=payload)
        assert response.status_code == 400

    def test_register_invalid_email_returns_422(self):
        """Sending an invalid email format → 422 Unprocessable Entity.

        This is Pydantic validation in action! The EmailStr type
        rejects 'not-an-email' before your function even runs.
        """
        response = client.post("/api/auth/register", json={
            "email": "not-an-email",
            "password": "password123"
        })
        assert response.status_code == 422

    def test_login_returns_jwt_token(self):
        """POST /api/auth/login with valid credentials → JWT token."""
        token = register_and_login()
        assert len(token) > 20  # JWT tokens are long strings

    def test_login_wrong_password_returns_401(self):
        """Wrong password → 401 Unauthorized."""
        # Register first
        client.post("/api/auth/register", json={
            "email": "user@example.com",
            "password": "correctpassword"
        })
        # Try wrong password
        response = client.post("/api/auth/login", json={
            "email": "user@example.com",
            "password": "wrongpassword"
        })
        assert response.status_code == 401

    def test_me_returns_user_profile(self):
        """GET /api/auth/me with valid token → user profile."""
        token = register_and_login()
        response = client.get(
            "/api/auth/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        assert response.json()["email"] == "test@example.com"

    def test_me_without_token_returns_401(self):
        """GET /api/auth/me without a token → 401 Unauthorized.

        This proves Dependency Injection (get_current_user) is working.
        """
        response = client.get("/api/auth/me")
        assert response.status_code == 401


# ---------------------------------------------------------------------------
# TEST SUITE 3: Document Upload (POST with file)
# ---------------------------------------------------------------------------

class TestUploadEndpoint:
    """Tests for POST /api/upload.

    Concepts demonstrated:
    - File upload via multipart/form-data
    - File type validation
    - File size validation
    - Auth-protected endpoint
    """

    def test_upload_requires_auth(self):
        """Uploading without a token → 401."""
        response = client.post("/api/upload", files={
            "file": ("test.txt", b"Some legal text here.", "text/plain")
        })
        assert response.status_code == 401

    def test_upload_txt_file(self):
        """Upload a .txt file → 200 with document data."""
        token = register_and_login()
        content = b"The Contractor shall indemnify and hold harmless the Client from all claims."
        response = client.post(
            "/api/upload",
            files={"file": ("contract.txt", content, "text/plain")},
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["filename"] == "contract.txt"
        assert "id" in data

    def test_upload_unsupported_format_returns_400(self):
        """Uploading a .jpg file → 400 Bad Request."""
        token = register_and_login()
        response = client.post(
            "/api/upload",
            files={"file": ("photo.jpg", b"fake image data", "image/jpeg")},
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 400

    def test_upload_empty_file_returns_400(self):
        """Uploading an empty file → 400 Bad Request."""
        token = register_and_login()
        response = client.post(
            "/api/upload",
            files={"file": ("empty.txt", b"", "text/plain")},
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 400


# ---------------------------------------------------------------------------
# TEST SUITE 4: Document Analysis (POST + GET)
# ---------------------------------------------------------------------------

class TestAnalyzeEndpoints:
    """Tests for /api/analyze/{id} and /api/clauses/*.

    Concepts demonstrated:
    - Path parameters ({document_id})
    - POST that triggers processing
    - GET that reads results
    - 404 for non-existent resources
    """

    def _upload_document(self, token: str) -> int:
        """Helper: Upload a document and return its ID."""
        content = (
            b"SECTION 1: INDEMNIFICATION. "
            b"The Contractor shall defend, indemnify, and hold harmless "
            b"the Client from and against any and all third-party claims. "
            b"SECTION 2: TERMINATION. "
            b"Either party may terminate this agreement with 30 days written notice."
        )
        response = client.post(
            "/api/upload",
            files={"file": ("nda.txt", content, "text/plain")},
            headers={"Authorization": f"Bearer {token}"}
        )
        return response.json()["id"]

    def test_analyze_nonexistent_document_returns_404(self):
        """Analyzing a document that doesn't exist → 404."""
        token = register_and_login()
        response = client.post(
            "/api/analyze/99999",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 404

    def test_analyze_extracts_clauses(self):
        """Analyzing a document should extract and return clauses."""
        token = register_and_login()
        doc_id = self._upload_document(token)

        response = client.post(
            f"/api/analyze/{doc_id}",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        clauses = response.json()
        assert isinstance(clauses, list)
        assert len(clauses) > 0

        # Each clause should have these fields
        first_clause = clauses[0]
        assert "clause_text" in first_clause
        assert "clause_type" in first_clause
        assert "risk_score" in first_clause
        assert "risk_level" in first_clause

    def test_get_clauses_by_document(self):
        """GET /api/clauses/{doc_id} should return clauses for that document."""
        token = register_and_login()
        doc_id = self._upload_document(token)
        headers = {"Authorization": f"Bearer {token}"}

        # First analyze the document
        client.post(f"/api/analyze/{doc_id}", headers=headers)

        # Then fetch clauses
        response = client.get(f"/api/clauses/{doc_id}", headers=headers)
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_get_documents_list(self):
        """GET /api/documents should return all uploaded documents."""
        token = register_and_login()
        headers = {"Authorization": f"Bearer {token}"}
        self._upload_document(token)

        response = client.get("/api/documents", headers=headers)
        assert response.status_code == 200
        docs = response.json()
        assert len(docs) >= 1
        assert "filename" in docs[0]
        assert "clause_count" in docs[0]


# ---------------------------------------------------------------------------
# TEST SUITE 5: Analytics (GET)
# ---------------------------------------------------------------------------

class TestAnalyticsEndpoint:
    """Tests for GET /api/analytics.

    This endpoint aggregates data across all documents.
    """

    def test_analytics_returns_stats(self):
        """Analytics should return risk distribution and counts."""
        token = register_and_login()
        headers = {"Authorization": f"Bearer {token}"}

        response = client.get("/api/analytics", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert "total_documents" in data
        assert "total_clauses" in data
        assert "risk_distribution" in data


# ---------------------------------------------------------------------------
# TEST SUITE 6: Search (GET with Query Parameters)
# ---------------------------------------------------------------------------

class TestSearchEndpoint:
    """Tests for GET /api/search?query=...&limit=...

    Concepts demonstrated:
    - Query parameters (not path parameters)
    - Default values (limit defaults to 10)
    """

    def test_search_returns_results(self):
        """Searching for a term should return matching clauses."""
        token = register_and_login()
        headers = {"Authorization": f"Bearer {token}"}

        # Upload and analyze a document first
        content = b"The Contractor shall indemnify and hold harmless the Client."
        client.post(
            "/api/upload",
            files={"file": ("test.txt", content, "text/plain")},
            headers=headers
        )
        doc_response = client.get("/api/documents", headers=headers)
        if doc_response.json():
            doc_id = doc_response.json()[0]["id"]
            client.post(f"/api/analyze/{doc_id}", headers=headers)

        response = client.get(
            "/api/search",
            params={"query": "indemnify", "limit": 5},
            headers=headers
        )
        assert response.status_code == 200
        data = response.json()
        assert "results" in data
        assert "query" in data
