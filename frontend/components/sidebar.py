### frontend/components/sidebar.py

import streamlit as st
from api_client import api_client

def render_sidebar():
    """Enhanced professional sidebar with modern navigation"""
    
    # Enhanced sidebar styling with consistent design
    st.markdown("""
    <style>
        /* Enhanced sidebar styling with consistent design */
        .sidebar-header {
            background: linear-gradient(135deg, #60a5fa 0%, #a78bfa 50%, #c084fc 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-size: 2rem;
            font-weight: 800;
            text-align: center;
            margin-bottom: 2rem;
            letter-spacing: -0.025em;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            text-shadow: 0 2px 8px rgba(96, 165, 250, 0.3);
        }
        .sidebar-section { 
            background: linear-gradient(135deg, rgba(59, 130, 246, 0.08), rgba(139, 92, 246, 0.06)); 
            border-radius: 16px; 
            padding: 1.5rem; 
            margin: 1rem 0; 
            border: 1px solid rgba(59, 130, 246, 0.2); 
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(10px);
            position: relative;
            overflow: hidden;
        }
        .sidebar-section::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 4px;
            height: 100%;
            background: linear-gradient(135deg, #3b82f6, #8b5cf6);
        }
        .status-indicator { 
            display: inline-flex; 
            align-items: center; 
            gap: 0.5rem; 
            padding: 0.7rem 1.2rem; 
            border-radius: 20px; 
            font-size: 0.9rem; 
            font-weight: 600; 
            margin-bottom: 1rem; 
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(10px);
            transition: all 0.3s ease;
        }
        .status-indicator:hover {
            transform: translateY(-1px);
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
        }
        .status-connected { 
            background: linear-gradient(135deg, #10b981 0%, #059669 100%); 
            color: #fff; 
        }
        .status-disconnected { 
            background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%); 
            color: #fff; 
        }
        .filter-section { 
            background: linear-gradient(135deg, rgba(59, 130, 246, 0.05), rgba(139, 92, 246, 0.03)); 
            border-radius: 12px; 
            padding: 1rem; 
            margin: 0.5rem 0; 
            border: 1px solid rgba(59, 130, 246, 0.15);
            backdrop-filter: blur(8px);
        }
        .metric-mini { 
            background: linear-gradient(135deg, rgba(59, 130, 246, 0.1), rgba(139, 92, 246, 0.08)); 
            border: 1px solid rgba(59, 130, 246, 0.2); 
            border-radius: 12px; 
            padding: 1rem; 
            text-align: center; 
            margin: 0.5rem 0; 
            transition: all 0.3s ease;
            backdrop-filter: blur(8px);
        }
        .metric-mini:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(59, 130, 246, 0.15);
            border-color: rgba(59, 130, 246, 0.3);
        }
        .metric-mini .value { 
            font-size: 1.8rem; 
            font-weight: 800; 
            background: linear-gradient(135deg, #60a5fa, #a78bfa); 
            -webkit-background-clip: text; 
            -webkit-text-fill-color: transparent; 
            background-clip: text; 
            display: block; 
            margin-bottom: 0.25rem;
        }
        .metric-mini .label { 
            font-size: 0.8rem; 
            color: #94a3b8; 
            text-transform: uppercase; 
            letter-spacing: 0.5px; 
            font-weight: 600;
        }
        /* Enhanced sidebar buttons */
        .stButton > button {
            background: linear-gradient(135deg, #3b82f6, #8b5cf6) !important;
            color: #ffffff !important;
            border: 1px solid rgba(59, 130, 246, 0.3) !important;
            padding: 0.7rem 1rem !important;
            border-radius: 12px !important;
            font-weight: 600 !important;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            box-shadow: 0 4px 15px rgba(59, 130, 246, 0.2) !important;
            backdrop-filter: blur(10px) !important;
            margin: 0.25rem 0 !important;
        }
        .stButton > button:hover {
            background: linear-gradient(135deg, #8b5cf6, #3b82f6) !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 25px rgba(59, 130, 246, 0.3) !important;
            border-color: rgba(139, 92, 246, 0.4) !important;
        }
        /* Enhanced sidebar headings */
        h4 {
            color: #ffffff !important;
            font-size: 1.2rem !important;
            font-weight: 700 !important;
            margin-bottom: 1rem !important;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        h4::before {
            content: '';
            width: 3px;
            height: 20px;
            background: linear-gradient(135deg, #3b82f6, #8b5cf6);
            border-radius: 2px;
        }
    </style>
    """, unsafe_allow_html=True)
    
    with st.sidebar:
        # Enhanced header with branding
        st.markdown('<h2 class="sidebar-header">LegalSight Pro</h2>', unsafe_allow_html=True)
        
        # Theme toggle
        theme = st.toggle("🌗 Light mode", value=st.session_state.get("theme", "Dark") == "Light", help="Toggle between light and dark themes")
        st.session_state["theme"] = "Light" if theme else "Dark"
        
        # API Status with enhanced styling
        connection_status = check_api_connection()
        if connection_status:
            st.markdown("""
            <div class="status-indicator status-connected">
                ✓ Backend Connected
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="status-indicator status-disconnected">
                ⚠ Backend Offline
            </div>
            """, unsafe_allow_html=True)
            st.markdown("""
            <div style="background: rgba(239, 68, 68, 0.1); border-radius: 8px; padding: 1rem; margin: 1rem 0;">
                <div style="color: #fca5a5; font-size: 0.9rem; line-height: 1.4;">
                    <strong>Setup Required:</strong><br>
                    <code>cd backend && python main.py</code>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Enhanced Navigation
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown('<h4>🧭 Navigation</h4>', unsafe_allow_html=True)
        
        nav_options = [
            ("🏠 Home", "Home"),
            ("📊 Dashboard", "Dashboard"),
            ("📤 Upload", "Upload"),
            ("📑 Clause Review", "Clause Review"),
            ("🔍 Search & Insights", "Search")
        ]
        current_page = st.session_state.get("current_page", "Home")
        for display_name, page_key in nav_options:
            if st.button(display_name, key=f"nav_{page_key}", use_container_width=True):
                st.session_state.current_page = page_key
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Filters
        if current_page in ["Dashboard", "Clause Review", "Search"] and connection_status:
            st.markdown("---")
            st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
            st.markdown('<h4>🔍 Filters & Options</h4>', unsafe_allow_html=True)
            st.markdown('<div class="filter-section">', unsafe_allow_html=True)
            risk_levels = st.multiselect(
                "Risk Levels",
                ["LOW", "MEDIUM", "HIGH"],
                default=st.session_state.filters.get("risk_levels", ["LOW", "MEDIUM", "HIGH"]),
                key=f"sidebar_risk_filter_{current_page}"
            )
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown('<div class="filter-section">', unsafe_allow_html=True)
            clause_types = st.multiselect(
                "Clause Types",
                ["INDEMNITY", "LIABILITY", "TERMINATION", "PAYMENT", "CONFIDENTIALITY", "INTELLECTUAL_PROPERTY", "GENERAL"],
                default=st.session_state.filters.get("clause_types", ["INDEMNITY", "LIABILITY", "TERMINATION", "PAYMENT", "CONFIDENTIALITY", "INTELLECTUAL_PROPERTY", "GENERAL"]),
                key=f"sidebar_clause_type_filter_{current_page}"
            )
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Document and date filters
            st.markdown('<div class="filter-section">', unsafe_allow_html=True)
            docs = api_client.get_documents() or []
            doc_options = {d.get('filename', f"Doc {d.get('id')}"): d.get('id') for d in docs}
            selected_docs_names = st.multiselect("Documents", list(doc_options.keys()), help="Filter by specific documents", key=f"sidebar_doc_filter_{current_page}")
            selected_docs = [doc_options[name] for name in selected_docs_names]
            st.markdown('</div>', unsafe_allow_html=True)

            # Date filter temporarily disabled to fix None value issues
            # st.markdown('<div class="filter-section">', unsafe_allow_html=True)
            # date_range = st.date_input("Upload date range", value=date.today(), help="Filter analytics by upload date", key=f"sidebar_date_filter_{current_page}")
            # st.markdown('</div>', unsafe_allow_html=True)

            st.session_state["filters"] = {
                "risk_levels": risk_levels,
                "clause_types": clause_types,
                "documents": selected_docs,
                "date_range": None  # Temporarily disabled
            }
            if st.button("🔄 Apply Filters", type="primary", use_container_width=True):
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        
        # System metrics
        if connection_status:
            analytics = api_client.get_analytics()
            if analytics:
                st.markdown("---")
                st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
                st.markdown('<h4>📈 System Overview</h4>', unsafe_allow_html=True)
                st.markdown(f"""
                <div class="metric-mini">
                    <span class="value">{analytics.get('total_documents', 0)}</span>
                    <span class="label">Documents</span>
                </div>
                """, unsafe_allow_html=True)
                st.markdown(f"""
                <div class="metric-mini">
                    <span class="value">{analytics.get('total_clauses', 0)}</span>
                    <span class="label">Clauses</span>
                </div>
                """, unsafe_allow_html=True)
                if analytics.get('total_clauses', 0) > 0:
                    high_risk_pct = analytics.get('high_risk_percentage', 0)
                    st.markdown(f"""
                    <div class="metric-mini">
                        <span class="value">{high_risk_pct:.1f}%</span>
                        <span class="label">High Risk</span>
                    </div>
                    """, unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
        
        # Footer
        st.markdown("---")
        st.markdown("""
        <div style=\"text-align: center; color: #64748b; font-size: 0.8rem;\">
            <div style=\"margin-bottom: 0.5rem;\">
                <strong>LegalSight Pro</strong><br>
                AI Legal Analytics Platform
            </div>
            <div style=\"color: #94a3b8;\">
                v2.0 Enterprise Edition
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    return current_page

def check_api_connection():
    """Check API connection with enhanced error handling"""
    if "api_status" not in st.session_state or st.sidebar.button("🔄 Refresh", key="refresh_connection"):
        try:
            st.session_state.api_status = api_client.check_health()
        except Exception:
            st.session_state.api_status = False
    return st.session_state.api_status