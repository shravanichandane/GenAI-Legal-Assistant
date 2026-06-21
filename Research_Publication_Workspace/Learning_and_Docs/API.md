# API Documentation

## Overview
The Legal Document Review Assistant API provides RESTful endpoints for document upload, analysis, and search functionality.

## Base URL
```
http://localhost:8000
```

## Authentication
Currently, the API does not require authentication. In production, implement proper authentication mechanisms.

## Endpoints

### Health Check
#### GET /health
Check if the API is running.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T00:00:00Z"
}
```

### Document Upload
#### POST /api/upload
Upload and process a legal document.

**Request:**
- Content-Type: `multipart/form-data`
- Body: File upload with `file` field

**Response:**
```json
{
  "id": 1,
  "filename": "contract.pdf",
  "upload_date": "2024-01-01T00:00:00Z",
  "file_size": 1024000,
  "status": "processed"
}
```

#### GET /api/documents
Get list of all uploaded documents.

**Response:**
```json
[
  {
    "id": 1,
    "filename": "contract.pdf",
    "upload_date": "2024-01-01T00:00:00Z",
    "file_size": 1024000,
    "clause_count": 15,
    "high_risk_count": 3
  }
]
```

### Analysis
#### POST /api/analyze/{document_id}
Analyze a document to extract clauses.

**Parameters:**
- `document_id` (path): ID of the document to analyze

**Response:**
```json
[
  {
    "id": 1,
    "document_id": 1,
    "clause_text": "The Company shall indemnify...",
    "clause_type": "INDEMNITY",
    "risk_level": "HIGH",
    "risk_score": 8.5,
    "summary": "This clause requires the Company to...",
    "reasoning": "High risk due to unlimited liability..."
  }
]
```

#### GET /api/clauses
Get all extracted clauses.

**Query Parameters:**
- `document_id` (optional): Filter by document ID
- `risk_level` (optional): Filter by risk level (LOW, MEDIUM, HIGH)
- `clause_type` (optional): Filter by clause type

**Response:**
```json
[
  {
    "id": 1,
    "document_id": 1,
    "clause_text": "The Company shall indemnify...",
    "clause_type": "INDEMNITY",
    "risk_level": "HIGH",
    "risk_score": 8.5,
    "summary": "This clause requires the Company to...",
    "reasoning": "High risk due to unlimited liability...",
    "document_filename": "contract.pdf"
  }
]
```

#### PUT /api/clauses/{clause_id}
Update a clause.

**Parameters:**
- `clause_id` (path): ID of the clause to update

**Request Body:**
```json
{
  "clause_text": "Updated clause text...",
  "clause_type": "LIABILITY",
  "risk_level": "MEDIUM",
  "risk_score": 6.0,
  "summary": "Updated summary...",
  "notes": "Additional notes..."
}
```

**Response:**
```json
{
  "id": 1,
  "document_id": 1,
  "clause_text": "Updated clause text...",
  "clause_type": "LIABILITY",
  "risk_level": "MEDIUM",
  "risk_score": 6.0,
  "summary": "Updated summary...",
  "notes": "Additional notes...",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

### Search
#### POST /api/search
Perform semantic search across clauses.

**Request Body:**
```json
{
  "query": "liability and indemnification",
  "limit": 10,
  "filters": {
    "risk_level": ["HIGH", "MEDIUM"],
    "clause_type": ["LIABILITY", "INDEMNITY"]
  }
}
```

**Response:**
```json
[
  {
    "id": 1,
    "document_id": 1,
    "clause_text": "The Company shall indemnify...",
    "clause_type": "INDEMNITY",
    "risk_level": "HIGH",
    "relevance_score": 0.95,
    "summary": "This clause requires the Company to...",
    "document_filename": "contract.pdf"
  }
]
```

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Invalid file format. Supported formats: PDF, DOCX, TXT"
}
```

### 404 Not Found
```json
{
  "detail": "Document not found"
}
```

### 422 Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "clause_type"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

## Rate Limiting
Currently, no rate limiting is implemented. In production, implement appropriate rate limiting based on your requirements.

## CORS
The API is configured to allow requests only from the Streamlit frontend (`http://localhost:8501`). Update `backend/main.py` to add your production domain when deploying.
