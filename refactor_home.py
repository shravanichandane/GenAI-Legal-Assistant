import re

with open("frontend/app.py", "r", encoding="utf-8") as f:
    content = f.read()

home_start = content.find('def render_home_page():')
home_end = content.find('def render_dashboard_page():')

new_home_page = """def render_home_page():
    # Targeted CSS for hover effects on cards
    st.markdown('''
        <style>
        .feature-card {
            transition: all 0.2s ease-in-out;
            padding: 1.5rem;
            border-radius: 0.5rem;
            background-color: white;
            border: 1px solid #e2e8f0;
            height: 100%;
        }
        .feature-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
            border-color: #2563eb;
        }
        .feature-icon {
            font-size: 2rem;
            margin-bottom: 1rem;
            color: #2563eb;
        }
        .feature-title {
            font-size: 1.25rem;
            font-weight: 600;
            color: #0f172a;
            margin-bottom: 0.5rem;
        }
        .feature-desc {
            color: #475569;
            font-size: 0.95rem;
            line-height: 1.5;
        }
        </style>
    ''', unsafe_allow_html=True)

    # Hero Section
    col_hero, col_img = st.columns([3, 2])
    with col_hero:
        st.markdown("<h1 style='font-size: 3rem; font-weight: 800; color: #0f172a; margin-bottom: 0.5rem;'>Elevate Your Legal Review.</h1>", unsafe_allow_html=True)
        st.markdown("<p style='font-size: 1.2rem; color: #475569; margin-bottom: 2rem; max-width: 600px;'>LegalSight Pro is an enterprise-grade AI platform that instantly analyzes contracts, identifies risks, and extracts critical clauses with pinpoint accuracy.</p>", unsafe_allow_html=True)
        
        col_btn1, col_btn2 = st.columns([1, 2])
        with col_btn1:
            if st.button("🚀 Upload Document", type="primary", use_container_width=True):
                st.session_state.current_page = "Upload"
                st.rerun()
        with col_btn2:
            if st.button("View Sample Dashboard", use_container_width=True):
                st.session_state.current_page = "Dashboard"
                st.rerun()
                
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    
    # Asymmetric Grid
    st.markdown("<h2 style='font-size: 1.5rem; color: #0f172a; margin-bottom: 1.5rem;'>Platform Capabilities</h2>", unsafe_allow_html=True)
    
    # Top row: 2 columns (Asymmetric)
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown('''
            <div class="feature-card">
                <div class="feature-icon">🧠</div>
                <div class="feature-title">Context-Aware AI Analysis</div>
                <div class="feature-desc">Our proprietary legal models read beyond keywords. They understand the semantic context of your agreements, identifying subtle indemnification risks and buried liabilities that standard tools miss.</div>
            </div>
        ''', unsafe_allow_html=True)
    with col2:
        st.markdown('''
            <div class="feature-card">
                <div class="feature-icon">⚡</div>
                <div class="feature-title">Real-Time Processing</div>
                <div class="feature-desc">Upload 100-page MSAs and receive comprehensive risk breakdowns in seconds, not hours.</div>
            </div>
        ''', unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
        
    # Bottom row: 3 equal columns
    col3, col4, col5 = st.columns(3)
    with col3:
        st.markdown('''
            <div class="feature-card">
                <div class="feature-icon">📊</div>
                <div class="feature-title">Interactive Dashboard</div>
                <div class="feature-desc">Visualize risk distribution across your entire portfolio with interactive charts and KPI metrics.</div>
            </div>
        ''', unsafe_allow_html=True)
    with col4:
        st.markdown('''
            <div class="feature-card">
                <div class="feature-icon">🔍</div>
                <div class="feature-title">Smart Search</div>
                <div class="feature-desc">Instantly locate specific obligations or force majeure clauses across thousands of documents.</div>
            </div>
        ''', unsafe_allow_html=True)
    with col5:
        st.markdown('''
            <div class="feature-card">
                <div class="feature-icon">🛡️</div>
                <div class="feature-title">Bank-Grade Security</div>
                <div class="feature-desc">SOC2 compliant infrastructure ensures your highly sensitive legal data remains strictly confidential.</div>
            </div>
        ''', unsafe_allow_html=True)

"""

if home_start != -1 and home_end != -1:
    content = content[:home_start] + new_home_page + content[home_end:]
    with open("frontend/app.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("Updated home page.")
else:
    print("Could not find boundaries.")
