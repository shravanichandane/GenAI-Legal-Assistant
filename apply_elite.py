import re

with open("frontend/app.py", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add import
if "from components.theme import apply_elite_theme" not in content:
    content = content.replace("from components.clause_editor import render_clause_editor", "from components.clause_editor import render_clause_editor\nfrom components.theme import apply_elite_theme")

# 2. Call apply_elite_theme()
if "apply_elite_theme()" not in content:
    marker = "# Ensure date_range is never an empty list or None"
    if marker in content:
        content = content.replace(marker, "apply_elite_theme()\n\n" + marker)

# 3. Replace Home Page
home_start = content.find('def render_home_page():')
home_end = content.find('def render_dashboard_page():')

new_home_page = """def render_home_page():
    # Hero Section
    col_hero, col_img = st.columns([3, 2])
    with col_hero:
        st.markdown("<h1 style='font-size: 3.5rem; font-weight: 800; color: #1E3A8A; margin-bottom: 0.5rem; line-height: 1.1;'>Elevate Your Legal Review.</h1>", unsafe_allow_html=True)
        st.markdown("<p style='font-size: 1.2rem; color: #334155; margin-bottom: 2rem; max-width: 600px;'>LegalSight Pro is an elite enterprise platform that instantly analyzes contracts, identifies risks, and extracts critical clauses with pinpoint accuracy.</p>", unsafe_allow_html=True)
        
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
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown('''
            <div class="elite-card">
                <div style="font-size: 2rem; color: #1E3A8A; margin-bottom: 1rem;">🧠</div>
                <h3 style="color: #0f172a; margin-top: 0;">Context-Aware AI Analysis</h3>
                <p style="color: #475569;">Our proprietary legal models read beyond keywords. They understand the semantic context of your agreements, identifying subtle indemnification risks and buried liabilities that standard tools miss.</p>
            </div>
        ''', unsafe_allow_html=True)
    with col2:
        st.markdown('''
            <div class="elite-card">
                <div style="font-size: 2rem; color: #1E3A8A; margin-bottom: 1rem;">⚡</div>
                <h3 style="color: #0f172a; margin-top: 0;">Real-Time Processing</h3>
                <p style="color: #475569;">Upload 100-page MSAs and receive comprehensive risk breakdowns in seconds, not hours.</p>
            </div>
        ''', unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
        
    col3, col4, col5 = st.columns(3)
    with col3:
        st.markdown('''
            <div class="elite-card">
                <div style="font-size: 2rem; color: #1E3A8A; margin-bottom: 1rem;">📊</div>
                <h3 style="color: #0f172a; margin-top: 0;">Interactive Dashboard</h3>
                <p style="color: #475569;">Visualize risk distribution across your entire portfolio with interactive charts and KPI metrics.</p>
            </div>
        ''', unsafe_allow_html=True)
    with col4:
        st.markdown('''
            <div class="elite-card">
                <div style="font-size: 2rem; color: #1E3A8A; margin-bottom: 1rem;">🔍</div>
                <h3 style="color: #0f172a; margin-top: 0;">Smart Search</h3>
                <p style="color: #475569;">Instantly locate specific obligations or force majeure clauses across thousands of documents.</p>
            </div>
        ''', unsafe_allow_html=True)
    with col5:
        st.markdown('''
            <div class="elite-card">
                <div style="font-size: 2rem; color: #1E3A8A; margin-bottom: 1rem;">🛡️</div>
                <h3 style="color: #0f172a; margin-top: 0;">Bank-Grade Security</h3>
                <p style="color: #475569;">SOC2 compliant infrastructure ensures your highly sensitive legal data remains strictly confidential.</p>
            </div>
        ''', unsafe_allow_html=True)

"""
if home_start != -1 and home_end != -1:
    content = content[:home_start] + new_home_page + content[home_end:]

# 4. Update Dashboard KPI Cards
# In render_dashboard_page, find the KPI section
kpi_target = '''    # Enhanced KPI Cards with animations
    st.markdown("### 📈 Key Performance Indicators")
    col1, col2, col3, col4, col5 = st.columns(5)'''
kpi_replacement = '''    # Enhanced KPI Cards with animations
    st.markdown("### 📈 Executive Overview")
    col1, col2, col3, col4, col5 = st.columns(5)'''
content = content.replace(kpi_target, kpi_replacement)

# We will just replace st.metric with elite cards in the dashboard.
# Find the block where st.metric is used for Documents, Clauses, etc.
# Wait, let's just write a regex or replace the specific block.
metric_block_target = '''    with col1:
        st.metric(
            "📄 Total Documents", 
            len(documents),
            delta=f"+{len(documents)} this session" if len(documents) > 0 else None
        )
    
    with col2:
        st.metric(
            "📋 Total Clauses",
            len(clauses)
        )'''
        
metric_block_replacement = '''    with col1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Total Documents</div>
            <div class="kpi-value">{len(documents)}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Total Clauses</div>
            <div class="kpi-value">{len(clauses)}</div>
        </div>
        """, unsafe_allow_html=True)'''

content = content.replace(metric_block_target, metric_block_replacement)

# 5. Update Clause Review to use .legal-serif
clause_target = '''                with st.expander(f"🔍 {clause.get('clause_type', 'Unknown')} - Risk: {clause.get('risk_level', 'Unknown')}"):
                    st.markdown(f"""
                    **Original Text:**
                    {clause.get('clause_text', '')}
                    
                    **Summary:**
                    {clause.get('summary', 'No summary available')}
                    """)'''
                    
clause_replacement = '''                with st.expander(f"🔍 {clause.get('clause_type', 'Unknown')} - Risk: {clause.get('risk_level', 'Unknown')}"):
                    st.markdown(f"""
                    <div style="margin-bottom: 0.5rem; font-weight: 600; color: #334155;">Original Text:</div>
                    <div class="legal-serif">{clause.get('clause_text', '')}</div>
                    
                    <div style="margin-top: 1rem; margin-bottom: 0.5rem; font-weight: 600; color: #334155;">Summary:</div>
                    <div style="color: #475569;">{clause.get('summary', 'No summary available')}</div>
                    """, unsafe_allow_html=True)'''

content = content.replace(clause_target, clause_replacement)

# Also update the dashboard recent clauses
recent_target = '''                    with st.expander(f"🔍 {clause.get('clause_type', 'Unknown')} - Risk: {clause.get('risk_level', 'Unknown')}"):
                        st.markdown(f"""
                        <div class="clause-preview">
                            <p><strong>Document:</strong> {clause.get('document_filename', 'Unknown')}</p>
                            <p><strong>Summary:</strong> {clause.get('summary', 'No summary available')}</p>
                            <div class="clause-metrics">
                                <span class="risk-badge" style="background-color: {risk_color}20; color: {risk_color}; padding: 0.3rem 0.8rem; border-radius: 20px; font-size: 0.8rem;">
                                    Risk: {clause.get('risk_level', 'Unknown')} ({clause.get('risk_score', 'N/A')})
                                </span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)'''

recent_replacement = '''                    with st.expander(f"🔍 {clause.get('clause_type', 'Unknown')} - Risk: {clause.get('risk_level', 'Unknown')}"):
                        st.markdown(f"""
                        <div class="clause-preview" style="padding: 1rem;">
                            <p style="color: #64748b; font-size: 0.9rem;"><strong>Document:</strong> {clause.get('document_filename', 'Unknown')}</p>
                            <div class="legal-serif" style="margin: 1rem 0;">{clause.get('clause_text', 'Text not available in preview')}</div>
                            <p style="color: #475569;"><strong>Summary:</strong> {clause.get('summary', 'No summary available')}</p>
                            <div class="clause-metrics" style="margin-top: 1rem;">
                                <span class="risk-badge" style="background-color: {risk_color}15; color: {risk_color}; padding: 0.4rem 1rem; border-radius: 99px; font-weight: 600; font-size: 0.85rem; border: 1px solid {risk_color}40;">
                                    Risk: {clause.get('risk_level', 'Unknown')} ({clause.get('risk_score', 'N/A')})
                                </span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)'''

content = content.replace(recent_target, recent_replacement)

with open("frontend/app.py", "w", encoding="utf-8") as f:
    f.write(content)
print("Applied Elite Theme modifications to app.py")
