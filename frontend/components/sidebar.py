### frontend/components/sidebar.py

import streamlit as st
from api_client import api_client

def render_sidebar():
    """Enhanced professional sidebar with native Streamlit components"""
    
    with st.sidebar:
        # Simple native title
        st.title("⚖️ LegalSight Pro")
        
        # API Status
        connection_status = check_api_connection()
        if connection_status:
            st.success("Backend Connected 🟢", icon="✅")
        else:
            st.error("Backend Offline 🔴", icon="⚠")
            st.info("Setup Required:\n`cd backend && python main.py`")
        
        # User profile section
        current_user = st.session_state.get("current_user")
        if current_user:
            st.divider()
            user_name = current_user.get("full_name", "User")
            user_email = current_user.get("email", "")
            
            # Clean user profile using native markdown
            st.markdown(f"**👤 {user_name}**")
            st.markdown(f"*{user_email}*")
            
            if st.button("🚪 Logout", key="logout_btn", use_container_width=True):
                api_client.logout()
                st.rerun()
            st.divider()
        
        # Enhanced Navigation
        st.subheader("🧭 Navigation")
        
        nav_options = [
            ("🏠 Home", "Home"),
            ("📊 Dashboard", "Dashboard"),
            ("📤 Upload", "Upload"),
            ("📑 Clause Review", "Clause Review"),
            ("🔍 Search & Insights", "Search")
        ]
        current_page = st.session_state.get("current_page", "Home")
        
        for display_name, page_key in nav_options:
            if st.button(display_name, key=f"nav_{page_key}", use_container_width=True, type="primary" if current_page == page_key else "secondary"):
                st.session_state.current_page = page_key
                st.rerun()
        
        # Filters
        if current_page in ["Dashboard", "Clause Review", "Search"] and connection_status:
            st.divider()
            st.subheader("🔍 Filters & Options")
            
            risk_levels = st.multiselect(
                "Risk Levels",
                ["LOW", "MEDIUM", "HIGH"],
                default=st.session_state.filters.get("risk_levels", ["LOW", "MEDIUM", "HIGH"]),
                key=f"sidebar_risk_filter_{current_page}"
            )
            
            clause_types = st.multiselect(
                "Clause Types",
                ["INDEMNITY", "LIABILITY", "TERMINATION", "PAYMENT", "CONFIDENTIALITY", "INTELLECTUAL_PROPERTY", "GENERAL"],
                default=st.session_state.filters.get("clause_types", ["INDEMNITY", "LIABILITY", "TERMINATION", "PAYMENT", "CONFIDENTIALITY", "INTELLECTUAL_PROPERTY", "GENERAL"]),
                key=f"sidebar_clause_type_filter_{current_page}"
            )
            
            # Document filter
            docs = api_client.get_documents() or []
            doc_options = {d.get('filename', f"Doc {d.get('id')}"): d.get('id') for d in docs}
            selected_docs_names = st.multiselect("Documents", list(doc_options.keys()), help="Filter by specific documents", key=f"sidebar_doc_filter_{current_page}")
            selected_docs = [doc_options[name] for name in selected_docs_names]

            st.session_state["filters"] = {
                "risk_levels": risk_levels,
                "clause_types": clause_types,
                "documents": selected_docs,
                "date_range": None  # Temporarily disabled
            }
            if st.button("🔄 Apply Filters", type="primary", use_container_width=True):
                st.rerun()
        
        # System metrics
        if connection_status:
            analytics = api_client.get_analytics()
            if analytics:
                st.divider()
                if analytics.get('total_documents', 0) > 0:
                    st.subheader("📈 System Overview")
                    col1, col2 = st.columns(2)
                    col1.metric("Documents", analytics.get('total_documents', 0))
                    col2.metric("Clauses", analytics.get('total_clauses', 0))
                    
                    if analytics.get('total_clauses', 0) > 0:
                        high_risk_pct = analytics.get('high_risk_percentage', 0)
                        st.metric("High Risk", f"{high_risk_pct:.1f}%")
                else:
                    st.info("👋 Welcome! Navigate to the Upload page to add your first document.")
        
    return current_page

def check_api_connection():
    """Check API connection with enhanced error handling"""
    if "api_status" not in st.session_state or st.sidebar.button("🔄 Refresh Connection & Data", key="refresh_connection", use_container_width=True):
        try:
            st.cache_data.clear()
            st.session_state.api_status = api_client.check_health()
        except Exception:
            st.session_state.api_status = False
    return st.session_state.api_status