"""
===========================================================================
MODULE 0.2 — FastAPI Reference Guide
===========================================================================

This file is a TEACHING DOCUMENT, not production code.  Read it top to
bottom like a textbook chapter.  Every concept used in your existing
backend is explained here with runnable examples.

After reading this, you should be able to answer:

1. What problem does FastAPI solve?
   → It turns Python functions into HTTP endpoints that any client
     (browser, Streamlit, mobile app) can call over the network.

2. Why FastAPI over Flask or Django?
   → Automatic request validation (Pydantic), async support, and
     auto-generated API docs at /docs.  Flask requires extensions for
     each of these.  Django is heavier and opinionated about ORMs.

3. How does it work internally?
   → FastAPI is built on Starlette (ASGI server) and Pydantic (data
     validation).  When a request arrives:
       Request → Starlette routes it → Pydantic validates the body
       → Your function runs → Pydantic serialises the response → JSON

4. What alternatives exist?
   → Flask, Django REST Framework, Litestar, Sanic, Tornado.

5. What metrics evaluate it?
   → Response time (ms), request throughput (req/s), error rate (%).

6. How would I explain it in an interview?
   → "I built a RESTful API with FastAPI that exposes endpoints for
      document upload, clause analysis, and risk scoring.  FastAPI's
      Pydantic integration gives me automatic request validation and
      OpenAPI documentation, which reduced frontend-backend integration
      bugs to near zero."

===========================================================================
"""

# ── CONCEPT 1: HTTP Methods ─────────────────────────────────────────────
#
# HTTP is a protocol for communication between a client and a server.
# There are 4 main methods (verbs) you need to know:
#
#   GET    → Read data         (e.g., fetch all documents)
#   POST   → Create data       (e.g., upload a new document)
#   PUT    → Update data       (e.g., edit a clause's risk level)
#   DELETE → Remove data       (e.g., delete a document)
#
# Interview Tip:
#   Q: "What's the difference between PUT and PATCH?"
#   A: PUT replaces the ENTIRE resource.  PATCH updates only the
#      fields you send.  Your existing `update_clause` endpoint
#      actually behaves like PATCH (it uses `exclude_unset=True`).
#


# ── CONCEPT 2: Request & Response ────────────────────────────────────────
#
# Every HTTP interaction has two halves:
#
#   REQUEST  = What the client sends
#     - Method (GET, POST, etc.)
#     - URL path (/api/upload)
#     - Headers (Authorization: Bearer <token>)
#     - Body (JSON data or file upload)
#
#   RESPONSE = What the server sends back
#     - Status Code (200 OK, 201 Created, 400 Bad Request, 404 Not Found, 500 Server Error)
#     - Headers (Content-Type: application/json)
#     - Body (JSON data)
#
# Your existing code already uses these!  Look at `upload.py`:
#   - Request:  POST /api/upload with a file in the body
#   - Response: 200 with JSON DocumentResponse, or 400/500 with error detail
#


# ── CONCEPT 3: Pydantic Schemas ──────────────────────────────────────────
#
# Pydantic is the "bouncer at the door" for your API.
# It validates incoming data BEFORE your function even runs.
#
# Example from YOUR code (backend/models.py):
#
#   class ClauseBase(BaseModel):
#       clause_text: str                      # REQUIRED string
#       risk_score: Optional[float] = 0.0     # Optional, defaults to 0.0
#       risk_level: Optional[str] = "LOW"     # Optional, defaults to "LOW"
#
# If someone sends { "risk_score": "not a number" }, Pydantic will
# reject it with a 422 Unprocessable Entity BEFORE your code runs.
#
# Interview Tip:
#   Q: "Why use Pydantic instead of just checking types manually?"
#   A: Pydantic gives you:
#      - Automatic type coercion (string "3.5" → float 3.5)
#      - Nested validation (lists of objects, optional fields)
#      - Serialisation (.dict(), .json())
#      - OpenAPI schema generation (powers the /docs page)
#      Manual checks would require hundreds of lines and miss edge cases.
#

from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime


class ExampleClauseRequest(BaseModel):
    """Example: What the client sends when creating a clause."""
    clause_text: str
    clause_type: Optional[str] = "GENERAL"
    risk_score: Optional[float] = 0.0


class ExampleClauseResponse(BaseModel):
    """Example: What the server sends back."""
    id: int
    clause_text: str
    clause_type: str
    risk_score: float
    risk_level: str
    created_at: datetime

    class Config:
        from_attributes = True  # Allows SQLAlchemy models → Pydantic


# ── CONCEPT 4: Dependency Injection ──────────────────────────────────────
#
# This is the most POWERFUL concept in FastAPI and the hardest for
# beginners to grasp.
#
# Problem: Every route needs a database session AND the current user.
#          You don't want to write db = SessionLocal() in every function.
#
# Solution: FastAPI's Depends() automatically calls a function and
#           passes its return value to your route.
#
# YOUR CODE uses two dependencies:
#
#   1. get_db()          → Opens a database session, yields it, then closes it
#   2. get_current_user() → Reads the JWT token, decodes it, returns User
#
# Example from YOUR code (backend/routes/analyze.py):
#
#   @router.get("/clauses")
#   async def get_all_clauses(
#       db: Session = Depends(get_db),              ← DI provides the DB
#       current_user: User = Depends(get_current_user)  ← DI provides the User
#   ):
#       clauses = db.query(Clause).all()
#       return clauses
#
# What happens step by step:
#   1. Client sends GET /api/clauses with Authorization header
#   2. FastAPI calls get_current_user() → decodes JWT → returns User object
#   3. FastAPI calls get_db() → creates a Session
#   4. YOUR function runs with both injected
#   5. After your function returns, get_db() closes the Session
#
# Interview Tip:
#   Q: "Why use Dependency Injection instead of global variables?"
#   A: Three reasons:
#      - Testability: In tests, you can override Depends(get_db) with a
#        test database without changing production code.
#      - Lifecycle management: get_db() guarantees the session is closed
#        even if your function crashes (using try/finally).
#      - Composability: Dependencies can depend on other dependencies.
#        get_current_user depends on the JWT token, which depends on the
#        Authorization header.  FastAPI resolves the full chain for you.
#


# ── CONCEPT 5: APIRouter ────────────────────────────────────────────────
#
# As your API grows, you don't want 50 endpoints in one file.
# APIRouter lets you split routes into separate files (modules), then
# attach them to the main app.
#
# YOUR CODE does this in backend/main.py:
#
#   app.include_router(auth_router,   prefix="/api/auth",  tags=["Authentication"])
#   app.include_router(upload_router, prefix="/api",       tags=["Upload"])
#   app.include_router(analyze_router, prefix="/api",      tags=["Analysis"])
#
# The `prefix` parameter prepends to every route in that router.
# So `@router.post("/upload")` in upload.py becomes `/api/upload`.
#
# The `tags` parameter groups endpoints in the /docs page.
#


# ── CONCEPT 6: CORS (Cross-Origin Resource Sharing) ─────────────────────
#
# YOUR Streamlit frontend runs on localhost:8501.
# YOUR FastAPI backend runs on localhost:8000.
#
# Browsers block requests between different origins (port = different origin).
# CORS middleware tells the browser: "It's OK, let localhost:8501 talk to me."
#
# YOUR CODE does this in backend/main.py:
#
#   app.add_middleware(
#       CORSMiddleware,
#       allow_origins=["http://localhost:8501"],   ← Only your frontend
#       allow_credentials=True,                     ← Allow JWT cookies
#       allow_methods=["*"],                        ← GET, POST, PUT, DELETE
#       allow_headers=["*"],                        ← Authorization header
#   )
#
# Interview Tip:
#   Q: "Why not set allow_origins=['*'] in production?"
#   A: Because that would let ANY website make requests to your API,
#      which is a security vulnerability.  In production, you whitelist
#      only your known frontend domains.
#


# ── YOUR API MAP ─────────────────────────────────────────────────────────
#
# Here is the complete map of every endpoint in your existing backend:
#
# ┌─────────────────────────────────────────────────────────────────┐
# │ Method │ Path                  │ Purpose                       │
# ├────────┼───────────────────────┼───────────────────────────────┤
# │ GET    │ /health               │ Server health check           │
# │ POST   │ /api/auth/register    │ Create new user account       │
# │ POST   │ /api/auth/login       │ Authenticate, get JWT token   │
# │ GET    │ /api/auth/me          │ Get current user profile      │
# │ POST   │ /api/upload           │ Upload a document (PDF/DOCX)  │
# │ POST   │ /api/analyze/{id}     │ Extract & analyze clauses     │
# │ GET    │ /api/clauses          │ List all clauses              │
# │ GET    │ /api/clauses/{doc_id} │ List clauses for a document   │
# │ PUT    │ /api/clauses/{id}     │ Update a clause               │
# │ GET    │ /api/documents        │ List all documents            │
# │ GET    │ /api/analytics        │ Get risk distribution stats   │
# │ GET    │ /api/search?query=... │ Search clauses by text        │
# └─────────────────────────────────────────────────────────────────┘
#
# For the Tier 1 roadmap, we will ADD:
#   POST  /api/classify           → Classify a single clause (Legal-BERT)
#   GET   /api/contracts          → Alias for /api/documents (cleaner naming)
#
