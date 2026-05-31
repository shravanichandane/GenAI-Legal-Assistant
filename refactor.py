import re

with open("frontend/app.py", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Remove get_theme_colors and apply_enhanced_theme
# find start of get_theme_colors
start_idx = content.find("def get_theme_colors():")
# find end of apply_enhanced_theme which ends before "# API Helper Functions"
end_idx = content.find("# Navigation removed - using sidebar only")

if start_idx != -1 and end_idx != -1:
    content = content[:start_idx] + content[end_idx:]

# 2. Remove apply_enhanced_theme() call
content = content.replace("apply_enhanced_theme()", "")

# 3. Refactor render_login_page
login_start = content.find('def render_login_page():')
login_end = content.find('# Tab selector', login_start)

new_login_header = """def render_login_page():
    \"\"\"Render a premium login / register page\"\"\"
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.container(border=True):
            st.markdown("<h1 style='text-align: center;'>⚖️ LegalSight Pro</h1>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; color: #64748b;'>AI-Powered Legal Document Analysis</p>", unsafe_allow_html=True)
            st.divider()
            
"""
if login_start != -1 and login_end != -1:
    content = content[:login_start] + new_login_header + "    # Tab selector\n" + content[login_end + 14:]

# 4. Fix closing indentation for render_login_page since we added `with st.container(border=True):` inside `with col2:`
# Wait, no. We wrapped the header, not the form. So the form can stay outside the container, or we wrap everything in the container.
# If we wrap everything, it's harder with string replace. Our new_login_header just creates a container for the title.
# Let's fix it so it looks clean:

login_start = content.find('def render_login_page():')
login_end = content.find('# Main App', login_start)
# We can just write a completely new render_login_page to replace the old one.
new_login_page = """def render_login_page():
    \"\"\"Render a premium login / register page\"\"\"
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.container(border=True):
            st.markdown("<h1 style='text-align: center; color: #2563eb;'>⚖️ LegalSight Pro</h1>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; color: #64748b;'>Enterprise Legal Document Analysis</p>", unsafe_allow_html=True)
            st.divider()
            
            # Tab selector
            if "auth_tab" not in st.session_state:
                st.session_state.auth_tab = "Login"
            
            tab = st.radio("", ["Login", "Register"], horizontal=True, key="auth_mode_selector", label_visibility="collapsed")
            st.session_state.auth_tab = tab
            
            if st.session_state.auth_tab == "Login":
                with st.form("login_form"):
                    st.markdown("#### 🔐 Sign In")
                    email = st.text_input("Email", placeholder="you@example.com")
                    password = st.text_input("Password", type="password", placeholder="••••••••")
                    submitted = st.form_submit_button("Sign In", use_container_width=True, type="primary")
                    
                    if submitted:
                        if not email or not password:
                            st.error("Please fill in all fields.")
                        else:
                            result = api_client.login(email, password)
                            if result and result.get("access_token"):
                                st.success("✅ Login successful!")
                                st.rerun()
                            else:
                                st.error("❌ Invalid email or password.")
            
            else:  # Register
                with st.form("register_form"):
                    st.markdown("#### 📝 Create Account")
                    full_name = st.text_input("Full Name", placeholder="Jane Doe")
                    email = st.text_input("Email", placeholder="you@example.com")
                    password = st.text_input("Password", type="password", placeholder="Min 6 characters")
                    password_confirm = st.text_input("Confirm Password", type="password", placeholder="••••••••")
                    submitted = st.form_submit_button("Create Account", use_container_width=True, type="primary")
                    
                    if submitted:
                        if not full_name or not email or not password:
                            st.error("Please fill in all fields.")
                        elif len(password) < 6:
                            st.error("Password must be at least 6 characters.")
                        elif password != password_confirm:
                            st.error("Passwords do not match.")
                        else:
                            result = api_client.register(email, password, full_name)
                            if result and result.get("id"):
                                st.success("✅ Account created! You can now sign in.")
                                st.session_state.auth_tab = "Login"
                                st.rerun()

"""

if login_start != -1 and login_end != -1:
    content = content[:login_start] + new_login_page + content[login_end:]

# 5. Refactor render_home_page
home_start = content.find('def render_home_page():')
home_end = content.find('def render_dashboard_page():')
new_home_page = """def render_home_page():
    st.markdown("<h1 style='text-align: center;'>⚖️ Legal Document Review Assistant</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #64748b;'>AI-Powered Legal Document Analysis & Review Platform</p>", unsafe_allow_html=True)
    st.divider()
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Get Started", type="primary", use_container_width=True, key="get_started_btn"):
            st.session_state.current_page = "Upload"
            st.rerun()
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        with st.container(border=True):
            st.markdown("### 🤖 AI-Powered Analysis")
            st.write("Advanced AI algorithms analyze legal documents for risk assessment, clause identification, and compliance checking.")
    with col2:
        with st.container(border=True):
            st.markdown("### 📊 Interactive Dashboard")
            st.write("Comprehensive analytics dashboard with visualizations, trends, and insights for better decision making.")
    with col3:
        with st.container(border=True):
            st.markdown("### 🔍 Smart Search")
            st.write("Semantic search capabilities to find relevant clauses, documents, and legal precedents quickly.")
            
    col4, col5, col6 = st.columns(3)
    with col4:
        with st.container(border=True):
            st.markdown("### 📝 Clause Editor")
            st.write("Interactive clause editing with AI suggestions, risk highlighting, and collaborative review features.")
    with col5:
        with st.container(border=True):
            st.markdown("### ⚡ Real-time Processing")
            st.write("Fast document processing with real-time updates and instant feedback on document analysis.")
    with col6:
        with st.container(border=True):
            st.markdown("### 🔒 Secure & Compliant")
            st.write("Enterprise-grade security with compliance features for sensitive legal document handling.")

"""
if home_start != -1 and home_end != -1:
    content = content[:home_start] + new_home_page + content[home_end:]


# 6. Replace c = get_theme_colors() from everywhere
content = content.replace("c = get_theme_colors()", "")

with open("frontend/app.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Refactored frontend/app.py successfully!")
