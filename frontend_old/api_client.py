### frontend/api_client.py

import requests
import streamlit as st
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger(__name__)

class APIClient:
    def __init__(self, base_url: str = None):
        import os
        if base_url is None:
            try:
                # Try Streamlit secrets first, then environment variable, then localhost
                base_url = st.secrets.get("API_URL", os.environ.get("API_URL", "http://localhost:8000"))
            except Exception:
                # Fallback if st.secrets is not available
                base_url = os.environ.get("API_URL", "http://localhost:8000")
        self.base_url = base_url
        self.timeout = 30
    
    def _get_headers(self) -> Dict[str, str]:
        """Get request headers with auth token if available"""
        headers = {}
        token = st.session_state.get("auth_token")
        if token:
            headers["Authorization"] = f"Bearer {token}"
        return headers
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> Optional[Dict[Any, Any]]:
        """Make HTTP request with error handling and auth"""
        url = f"{self.base_url}{endpoint}"
        
        # Merge auth headers with any existing headers
        headers = self._get_headers()
        if "headers" in kwargs:
            headers.update(kwargs.pop("headers"))
        
        try:
            response = requests.request(method, url, timeout=self.timeout, headers=headers, **kwargs)
            
            if response.status_code == 200 or response.status_code == 201:
                return response.json()
            elif response.status_code == 401:
                # Token expired or invalid — clear auth state
                st.session_state.pop("auth_token", None)
                st.session_state.pop("current_user", None)
                if endpoint != "/api/auth/login":
                    st.error("Session expired. Please log in again.", icon="🚨")
                return None
            elif response.status_code == 404:
                st.error(f"Resource not found: {endpoint}")
                return None
            elif response.status_code == 400:
                error_detail = response.json().get('detail', 'Bad request')
                st.error(f"Request error: {error_detail}")
                return None
            else:
                st.error(f"API error {response.status_code}: {response.text}")
                return None
                
        except requests.exceptions.ConnectionError:
            st.error("🔌 Cannot connect to backend API. Please ensure FastAPI server is running on port 8000.")
            return None
        except requests.exceptions.Timeout:
            st.error("⏱️ Request timed out. Please try again.")
            return None
        except Exception as e:
            st.error(f"Unexpected error: {str(e)}")
            return None
    
    # ──────────────────────────────────────────
    # Authentication
    # ──────────────────────────────────────────
    
    def register(self, email: str, password: str, full_name: str) -> Optional[Dict[str, Any]]:
        """Register a new user"""
        return self._make_request("POST", "/api/auth/register", json={
            "email": email,
            "password": password,
            "full_name": full_name
        })
    
    def login(self, email: str, password: str) -> Optional[Dict[str, Any]]:
        """Login and get JWT token"""
        result = self._make_request("POST", "/api/auth/login", json={
            "email": email,
            "password": password
        })
        if result and result.get("access_token"):
            st.session_state["auth_token"] = result["access_token"]
            # Fetch user profile
            user = self.get_me()
            if user:
                st.session_state["current_user"] = user
        return result
    
    def get_me(self) -> Optional[Dict[str, Any]]:
        """Get current user profile"""
        return self._make_request("GET", "/api/auth/me")
    
    def logout(self):
        """Clear auth state"""
        st.session_state.pop("auth_token", None)
        st.session_state.pop("current_user", None)
    
    def is_authenticated(self) -> bool:
        """Check if user is currently authenticated"""
        return "auth_token" in st.session_state and st.session_state["auth_token"] is not None
    
    # ──────────────────────────────────────────
    # Health
    # ──────────────────────────────────────────
    
    def check_health(self) -> bool:
        """Check API health"""
        result = self._make_request("GET", "/health")
        return result is not None
    
    # ──────────────────────────────────────────
    # Documents & Clauses
    # ──────────────────────────────────────────
    
    def upload_document(self, uploaded_file) -> Optional[Dict[str, Any]]:
        """Upload document file"""
        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
        
        try:
            response = requests.post(
                f"{self.base_url}/api/upload", 
                files=files, 
                headers=self._get_headers(),
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 401:
                st.session_state.pop("auth_token", None)
                st.session_state.pop("current_user", None)
                st.error("Session expired. Please log in again.", icon="🚨")
                return None
            else:
                try:
                    error_detail = response.json().get('detail', 'Upload failed')
                except:
                    error_detail = f"HTTP {response.status_code}: {response.text}"
                st.error(f"Upload failed: {error_detail}")
                return {"error": error_detail}
                
        except Exception as e:
            st.error(f"Upload error: {str(e)}")
            return None
    
    def analyze_document(self, document_id: int) -> Optional[List[Dict[str, Any]]]:
        """Trigger document analysis"""
        return self._make_request("POST", f"/api/analyze/{document_id}")
    
    def get_documents(self) -> List[Dict[str, Any]]:
        """Fetch all documents"""
        result = self._make_request("GET", "/api/documents")
        return result if result is not None else []
    
    def get_document_clauses(self, document_id: int) -> List[Dict[str, Any]]:
        """Fetch clauses for a document"""
        result = self._make_request("GET", f"/api/clauses/{document_id}")
        return result if result is not None else []
    
    def get_clauses(self) -> List[Dict[str, Any]]:
        """Fetch all clauses"""
        result = self._make_request("GET", "/api/clauses")
        return result if result is not None else []
    
    def update_clause(self, clause_id: int, update_data: Dict[str, Any]) -> bool:
        """Update a clause"""
        result = self._make_request("PUT", f"/api/clauses/{clause_id}", json=update_data)
        return result is not None
    
    def search_clauses(self, query: str, limit: int = 10) -> Dict[str, Any]:
        """Search clauses"""
        result = self._make_request("GET", "/api/search", params={"query": query, "limit": limit})
        return result if result is not None else {"results": []}
    
    def get_analytics(self) -> Dict[str, Any]:
        """Get analytics data"""
        result = self._make_request("GET", "/api/analytics")
        return result if result is not None else {}

# Global API client instance
api_client = APIClient()
