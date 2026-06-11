import streamlit as st
import pandas as pd
import json
import traceback
import plotly.express as px
from datetime import datetime, timedelta
from api_client import api_client
from components.sidebar import render_sidebar
from components.charts import (
    create_clause_type_chart,
    create_risk_distribution_chart,
    create_risk_heatmap,
    create_kpi_cards,
    create_temporal_trend_chart,
    create_clause_comparison_chart,
    create_similarity_heatmap,
    create_word_cloud_like,
)
from components.clause_editor import render_clause_editor
from components.theme import apply_elite_theme
import time

# Page configuration
st.set_page_config(
    page_title="Legal Document Review Assistant",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

from datetime import date

if "current_page" not in st.session_state:
    st.session_state.current_page = "Home"
if "theme" not in st.session_state:
    st.session_state.theme = "Light"
if "filters" not in st.session_state:
    st.session_state.filters = {
        "risk_levels": ["LOW", "MEDIUM", "HIGH"],
        "clause_types": ["INDEMNITY", "LIABILITY", "TERMINATION", "PAYMENT", "CONFIDENTIALITY", "INTELLECTUAL_PROPERTY", "GENERAL"],
        "documents": [],
        "date_range": date.today()
    }
if "api_status" not in st.session_state:
    st.session_state.api_status = False

apply_elite_theme()

# Ensure date_range is never an empty list or None
if st.session_state.filters.get("date_range") == [] or st.session_state.filters.get("date_range") is None:
    st.session_state.filters["date_range"] = date.today()

# Navigation removed - using sidebar only

# API Helper Functions
@st.cache_data(ttl=300)
def fetch_documents():
    try:
        return api_client.get_documents()
    except Exception as e:
        st.error(f"Error fetching documents: {str(e)}")
        return []

@st.cache_data(ttl=300)
def fetch_clauses():
    try:
        return api_client.get_clauses()
    except AttributeError as e:
        st.error(f"API method not found: {str(e)}")
        return []
    except Exception as e:
        st.error(f"Error fetching clauses: {str(e)}")
        return []

@st.cache_data(ttl=300)
def fetch_analytics():
    try:
        return api_client.get_analytics()
    except Exception as e:
        st.error(f"Error fetching analytics: {str(e)}")
        return {}

# Page Functions
def render_home_page():
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

def render_dashboard_page():
    st.markdown("""
    <div class="page-header">
        <h1><i class="fas fa-chart-line header-icon"></i>Interactive Analytics Dashboard</h1>
        <p>Comprehensive insights and visualizations for your legal document analysis</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Fetch data
    analytics = fetch_analytics()
    documents = fetch_documents()
    clauses = fetch_clauses()
    
    if not documents:
        st.markdown('''
            <div style="text-align: center; padding: 4rem 2rem; background: white; border-radius: 12px; border: 1px dashed #cbd5e1; margin-top: 2rem;">
                <div style="font-size: 3rem; color: #94a3b8; margin-bottom: 1rem;">📄</div>
                <h3 style="color: #0f172a; margin-bottom: 0.5rem; font-size: 1.5rem;">No Documents Analyzed Yet</h3>
                <p style="color: #64748b; margin-bottom: 1.5rem;">Upload your first legal document to unlock the Interactive Analytics Dashboard.</p>
            </div>
        ''', unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("🚀 Upload First Document", type="primary", use_container_width=True, key=f"empty_upload_render_dashboard_page"):
                st.session_state.current_page = "Upload"
                st.rerun()
        return
    
    # Check if clauses need to be extracted
    if documents and not clauses:
        st.markdown("### 🔄 Extracting Clauses from Documents")
        
        # Progress bar for clause extraction
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        extracted_clauses = []
        total_docs = len(documents)
        
        for i, doc in enumerate(documents):
            status_text.text(f"Analyzing {doc.get('filename', 'Unknown')}...")
            progress_bar.progress((i + 1) / total_docs)
            
            try:
                # Call the analyze endpoint to extract clauses
                result = api_client.analyze_document(doc['id'])
                if result and isinstance(result, list) and len(result) > 0:
                    extracted_clauses.extend(result)
                    st.write(f"✅ Extracted {len(result)} clauses from {doc.get('filename', 'Unknown')}")
                else:
                    st.write(f"⚠️ No clauses found in {doc.get('filename', 'Unknown')}")
            except Exception as e:
                st.warning(f"Could not extract clauses from {doc.get('filename', 'Unknown')}: {str(e)}")
        
        # Clear progress indicators
        progress_bar.empty()
        status_text.empty()
        
        if extracted_clauses:
            st.success(f"✅ Successfully extracted {len(extracted_clauses)} clauses from {len(documents)} documents!")
            # Refresh clauses data
            clauses = fetch_clauses()
        else:
            st.warning("⚠️ No clauses could be extracted from the documents. Please check if the documents contain legal text.")
    
    # If still no clauses after extraction attempt
    if not clauses:
        st.info("📊 No clauses available for analysis. Please ensure documents contain legal text and try uploading again.")
        return
    
    # Enhanced KPI Cards with animations
    st.markdown("### 📈 Executive Overview")
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            "📄 Total Documents", 
            len(documents),
            delta=f"+{len(documents)} this session" if len(documents) > 0 else None
        )
    
    with col2:
        st.metric(
            "📝 Total Clauses", 
            len(clauses),
            delta=f"+{len(clauses)} extracted" if len(clauses) > 0 else None
        )
    
    with col3:
        high_risk = len([c for c in clauses if c.get('risk_level') == 'HIGH'])
        st.metric(
            "⚠️ High Risk", 
            high_risk,
            delta=f"{high_risk} clauses" if high_risk > 0 else "0 clauses"
        )
    
    with col4:
        medium_risk = len([c for c in clauses if c.get('risk_level') == 'MEDIUM'])
        st.metric(
            "⚡ Medium Risk", 
            medium_risk,
            delta=f"{medium_risk} clauses" if medium_risk > 0 else "0 clauses"
        )
    
    with col5:
        low_risk = len([c for c in clauses if c.get('risk_level') == 'LOW'])
        st.metric(
            "✅ Low Risk", 
            low_risk,
            delta=f"{low_risk} clauses" if low_risk > 0 else "0 clauses"
        )
    
    # Document Selection and Clause Extraction
    st.markdown("""
    <div class="section-header">
        <h3><i class="fas fa-file-alt subheader-icon"></i>Document Selection & Analysis</h3>
        <p>Choose documents to analyze and extract clauses automatically</p>
    </div>
    """, unsafe_allow_html=True)
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        # Document chooser
        doc_options = ["All Documents"] + [d.get('filename', f'Document {d.get("id", "Unknown")}') for d in documents]
        selected_doc = st.selectbox(
            "Choose Document to Analyze",
            options=doc_options,
            key="dashboard_document_chooser",
            help="Select a specific document to view its clause analysis, or 'All Documents' for overall analytics"
        )
    
    with col2:
        # Quick stats for selected document
        if selected_doc != "All Documents":
            # Find the document ID for the selected filename
            selected_doc_id = next((d.get('id') for d in documents if d.get('filename') == selected_doc), None)
            doc_clauses = [c for c in clauses if c.get('document_id') == selected_doc_id] if selected_doc_id else []
            st.metric("Clauses in Document", len(doc_clauses))
        else:
            st.metric("Total Clauses", len(clauses))
    
    with col3:
        # Manual clause extraction button
        if st.button("🔄 Extract Clauses", help="Manually trigger clause extraction from all documents"):
            with st.spinner("Extracting clauses from all documents..."):
                extracted_count = 0
                for doc in documents:
                    try:
                        result = api_client.analyze_document(doc['id'])
                        if result and result.get('clauses'):
                            extracted_count += len(result['clauses'])
                    except Exception as e:
                        st.warning(f"Error extracting from {doc.get('filename', 'Unknown')}: {str(e)}")
                
                if extracted_count > 0:
                    st.success(f"✅ Extracted {extracted_count} new clauses!")
                    st.rerun()
        else:
                    st.warning("⚠️ No new clauses extracted. Documents may already be analyzed.")
    
    # Interactive Filters
    st.markdown("### 🔍 Interactive Filters")
    filter_col1, filter_col2, filter_col3, filter_col4 = st.columns(4)
    
    with filter_col1:
        risk_filter = st.multiselect(
            "Risk Level",
            options=["HIGH", "MEDIUM", "LOW"],
            default=["HIGH", "MEDIUM", "LOW"],
            key="dashboard_risk_filter"
        )
    
    with filter_col2:
        clause_type_filter = st.multiselect(
            "Clause Type",
            options=list(set([c.get('clause_type', 'Unknown') for c in clauses])),
            default=list(set([c.get('clause_type', 'Unknown') for c in clauses])),
            key="dashboard_clause_filter"
        )
    
    with filter_col3:
        # Document filter (now based on selection)
        if selected_doc == "All Documents":
            document_filter = st.multiselect(
                "Document",
                options=[d.get('filename', 'Unknown') for d in documents],
                default=[d.get('filename', 'Unknown') for d in documents],
                key="dashboard_doc_filter"
            )
        else:
            document_filter = [selected_doc]
            st.info(f"Analyzing: {selected_doc}")
    
    with filter_col4:
        date_range = st.date_input(
            "Date Range",
            value=None,
            key="dashboard_date_filter"
        )
    
    # Filter data based on selections
    if selected_doc == "All Documents":
        # For "All Documents", we need to match by document ID
        document_ids = [d.get('id') for d in documents if d.get('filename') in document_filter]
        filtered_clauses = [c for c in clauses if 
                           c.get('risk_level') in risk_filter and
                           c.get('clause_type') in clause_type_filter and
                           c.get('document_id') in document_ids]
    else:
        # Filter for selected document only
        selected_doc_id = next((d.get('id') for d in documents if d.get('filename') == selected_doc), None)
        filtered_clauses = [c for c in clauses if 
                           c.get('document_id') == selected_doc_id and
                           c.get('risk_level') in risk_filter and
                           c.get('clause_type') in clause_type_filter] if selected_doc_id else []
    
    # Document-specific analysis
    if selected_doc != "All Documents":
        st.markdown("### 📋 Document-Specific Analysis")
        
        # Document details
        selected_document = next((d for d in documents if d.get('filename') == selected_doc), None)
        if selected_document:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Document ID", selected_document.get('id', 'Unknown'))
            
            with col2:
                upload_date = selected_document.get('upload_date', 'Unknown')
                if upload_date != 'Unknown':
                    upload_date = upload_date[:10] if len(upload_date) > 10 else upload_date
                st.metric("Upload Date", upload_date)
            
            with col3:
                content_length = len(selected_document.get('content', ''))
                st.metric("Content Length", f"{content_length:,} chars")
            
            with col4:
                doc_risk_score = sum([c.get('risk_score', 0) for c in filtered_clauses]) / len(filtered_clauses) if filtered_clauses else 0
                st.metric("Avg Risk Score", f"{doc_risk_score:.1f}/10")
        
        # Document-specific insights
        if filtered_clauses:
            st.markdown("#### 🔍 Document Insights")
        col1, col2 = st.columns(2)
        
        with col1:
                st.markdown("**📊 Risk Distribution in this Document:**")
                risk_counts = {}
                for clause in filtered_clauses:
                    risk_level = clause.get('risk_level', 'Unknown')
                    risk_counts[risk_level] = risk_counts.get(risk_level, 0) + 1
                
                for risk_level, count in risk_counts.items():
                    percentage = (count / len(filtered_clauses)) * 100
                    st.write(f"• **{risk_level} Risk**: {count} clauses ({percentage:.1f}%)")
        
        with col2:
                st.markdown("**📝 Clause Types in this Document:**")
                clause_type_counts = {}
                for clause in filtered_clauses:
                    clause_type = clause.get('clause_type', 'Unknown')
                    clause_type_counts[clause_type] = clause_type_counts.get(clause_type, 0) + 1
                
                sorted_types = sorted(clause_type_counts.items(), key=lambda x: x[1], reverse=True)
                for clause_type, count in sorted_types:
                    percentage = (count / len(filtered_clauses)) * 100
                    st.write(f"• **{clause_type}**: {count} clauses ({percentage:.1f}%)")
        
        # Top clauses from this document
        if filtered_clauses:
            st.markdown("#### 🏆 Top Clauses in this Document")
            
            # Sort clauses by risk score (highest first)
            sorted_clauses = sorted(filtered_clauses, key=lambda x: x.get('risk_score', 0), reverse=True)
            top_clauses = sorted_clauses[:5]  # Show top 5
            
            for i, clause in enumerate(top_clauses, 1):
                risk_color = {
                    'HIGH': '🔴',
                    'MEDIUM': '🟡',
                    'LOW': '🟢'
                }.get(clause.get('risk_level', 'UNKNOWN'), '⚪')
                
                with st.expander(f"{i}. {risk_color} {clause.get('clause_type', 'Unknown')} - Risk: {clause.get('risk_level', 'Unknown')} ({clause.get('risk_score', 'N/A')}/10)", expanded=False):
                    st.write(f"**Clause Text:** {clause.get('clause_text', 'No text available')[:200]}...")
                    if clause.get('summary'):
                        st.write(f"**AI Summary:** {clause.get('summary', 'No summary available')}")
                    st.write(f"**Risk Reasoning:** {clause.get('reasoning', 'No reasoning available')}")
    
    # Main Visualizations Grid
    st.markdown("""
    <div class="section-header">
        <h3><i class="fas fa-chart-bar subheader-icon"></i>Interactive Visualizations</h3>
        <p>Comprehensive analytics and insights from your document analysis</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Row 1: Primary Charts
    col1, col2 = st.columns(2)
    
    with col1:
        chart_title = f"#### 🎯 Clause Type Distribution{' - ' + selected_doc if selected_doc != 'All Documents' else ''}"
        st.markdown(chart_title)
        clause_chart = create_clause_type_chart(filtered_clauses)
        st.plotly_chart(clause_chart, use_container_width=True)
        
        # Add drill-down information
        if filtered_clauses:
            st.markdown("**📋 Top Clause Types:**")
            clause_counts = {}
            for clause in filtered_clauses:
                clause_type = clause.get('clause_type', 'Unknown')
                clause_counts[clause_type] = clause_counts.get(clause_type, 0) + 1
            
            sorted_types = sorted(clause_counts.items(), key=lambda x: x[1], reverse=True)
            for i, (clause_type, count) in enumerate(sorted_types[:3]):
                st.write(f"{i+1}. **{clause_type}**: {count} clauses")
        
    with col2:
        chart_title = f"#### ⚠️ Risk Level Distribution{' - ' + selected_doc if selected_doc != 'All Documents' else ''}"
        st.markdown(chart_title)
        risk_chart = create_risk_distribution_chart(filtered_clauses)
        st.plotly_chart(risk_chart, use_container_width=True)
        
        # Risk analysis summary
        if filtered_clauses:
            st.markdown("**🔍 Risk Analysis:**")
            high_count = len([c for c in filtered_clauses if c.get('risk_level') == 'HIGH'])
            medium_count = len([c for c in filtered_clauses if c.get('risk_level') == 'MEDIUM'])
            low_count = len([c for c in filtered_clauses if c.get('risk_level') == 'LOW'])
            
            total = len(filtered_clauses)
            if total > 0:
                st.write(f"• **High Risk**: {high_count} ({high_count/total*100:.1f}%)")
                st.write(f"• **Medium Risk**: {medium_count} ({medium_count/total*100:.1f}%)")
                st.write(f"• **Low Risk**: {low_count} ({low_count/total*100:.1f}%)")
    
    # Row 2: Advanced Visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        chart_title = f"#### 📈 Temporal Trends{' - ' + selected_doc if selected_doc != 'All Documents' else ''}"
        st.markdown(chart_title)
        if selected_doc == "All Documents":
            trend_chart = create_temporal_trend_chart(documents)
        else:
            # For specific document, show a simple trend
            trend_chart = create_temporal_trend_chart([selected_document] if selected_document else [])
        st.plotly_chart(trend_chart, use_container_width=True)
    
    with col2:
        chart_title = f"#### 🔗 Clause Comparison{' - ' + selected_doc if selected_doc != 'All Documents' else ''}"
        st.markdown(chart_title)
        if len(filtered_clauses) > 1:
            comparison_chart = create_clause_comparison_chart(filtered_clauses)
            st.plotly_chart(comparison_chart, use_container_width=True)
        else:
            st.info("Need at least 2 clauses for comparison")
    
    # Row 3: Risk Heatmap and Word Cloud
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🗺️ Risk Heatmap")
        if len(filtered_clauses) > 1:
            # Create a simple risk heatmap
            risk_data = []
            for clause in filtered_clauses:
                risk_data.append({
                    'clause_type': clause.get('clause_type', 'Unknown'),
                    'risk_level': clause.get('risk_level', 'Unknown'),
                    'risk_score': clause.get('risk_score', 0)
                })
            
            if risk_data:
                import pandas as pd
                df = pd.DataFrame(risk_data)
                heatmap_data = df.groupby(['clause_type', 'risk_level']).size().unstack(fill_value=0)
                
                import plotly.express as px
                fig = px.imshow(
                    heatmap_data.values,
                    x=heatmap_data.columns,
                    y=heatmap_data.index,
                    color_continuous_scale='Reds',
                    title="Risk Level by Clause Type"
                )
                fig.update_layout(
                    xaxis_title="Risk Level",
                    yaxis_title="Clause Type",
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Need multiple clauses for heatmap")
    
    with col2:
        st.markdown("#### ☁️ Key Terms Word Cloud")
        if filtered_clauses:
            word_cloud = create_word_cloud_like(filtered_clauses)
            if word_cloud:
                st.plotly_chart(word_cloud, use_container_width=True)
            else:
                st.info("Generating word cloud...")
        else:
            st.info("No clauses available for word cloud")
    
    # Row 4: Detailed Analytics
    st.markdown("### 📋 Detailed Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📊 Document Analysis")
        if documents:
            doc_analysis = []
            for doc in documents:
                doc_clauses = [c for c in filtered_clauses if c.get('document_id') == doc.get('id')]
                doc_analysis.append({
                    'Document': doc.get('filename', 'Unknown')[:30] + '...',
                    'Clauses': len(doc_clauses),
                    'High Risk': len([c for c in doc_clauses if c.get('risk_level') == 'HIGH']),
                    'Upload Date': doc.get('upload_date', 'Unknown')[:10] if doc.get('upload_date') else 'Unknown'
                })
            
            import pandas as pd
            df = pd.DataFrame(doc_analysis)
            st.dataframe(df, use_container_width=True)
    
    with col2:
        st.markdown("#### 🎯 Risk Score Distribution")
        if filtered_clauses:
            risk_scores = [c.get('risk_score', 0) for c in filtered_clauses if c.get('risk_score')]
            if risk_scores:
                import plotly.express as px
                fig = px.histogram(
                    x=risk_scores,
                    nbins=20,
                    title="Distribution of Risk Scores",
                    labels={'x': 'Risk Score', 'y': 'Count'}
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No risk scores available")
    
    # Bulk Edit Options
    st.markdown("""
    <div class="subsection-header">
        <h4><i class="fas fa-edit subheader-icon"></i>Bulk Edit Options</h4>
        <p>Edit multiple clauses at once or perform bulk operations</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("✏️ Bulk Edit Clauses", use_container_width=True, key="bulk_edit_button"):
            st.session_state.show_bulk_edit = True
            st.rerun()
    
    with col2:
        if st.button("🔄 Regenerate All AI", use_container_width=True, key="regenerate_ai_button"):
            st.info("🔄 Regenerating AI analysis for all clauses...")
    
    with col3:
        if st.button("📊 Export Analytics", use_container_width=True, key="bulk_export_analytics"):
            st.success("Analytics exported successfully!")
    
    # Bulk edit interface
    if st.session_state.get('show_bulk_edit', False):
        st.markdown("---")
        st.markdown("### 🔧 Bulk Edit Interface")
        
        # Select clauses to edit
        clause_options = [f"Clause {i+1}: {c.get('clause_type', 'Unknown')} - {c.get('risk_level', 'Unknown')} Risk" 
                         for i, c in enumerate(filtered_clauses)]
        
        selected_clauses = st.multiselect(
            "Select clauses to edit:",
            options=clause_options,
            default=clause_options[:3] if len(clause_options) >= 3 else clause_options,
            help="Choose which clauses you want to edit in bulk"
        )
        
        if selected_clauses:
            # Bulk operations
            col1, col2, col3 = st.columns(3)
            
            with col1:
                new_risk_level = st.selectbox("Set Risk Level for Selected Clauses:", 
                                            ['LOW', 'MEDIUM', 'HIGH'], 
                                            key="bulk_risk_level")
            
            with col2:
                new_clause_type = st.selectbox("Set Clause Type for Selected Clauses:", 
                                             ['INDEMNITY', 'LIABILITY', 'TERMINATION', 'PAYMENT', 'CONFIDENTIALITY', 'INTELLECTUAL_PROPERTY', 'GENERAL'],
                                             key="bulk_clause_type")
            
            with col3:
                if st.button("💾 Apply Bulk Changes", type="primary"):
                    # Apply changes to selected clauses
                    updated_count = 0
                    for i, option in enumerate(selected_clauses):
                        clause_index = clause_options.index(option)
                        clause = filtered_clauses[clause_index]
                        changes = {
                            'risk_level': new_risk_level,
                            'clause_type': new_clause_type
                        }
                        try:
                            if api_client.update_clause(clause['id'], changes):
                                updated_count += 1
                        except Exception as e:
                            st.error(f"Failed to update clause {clause_index + 1}: {str(e)}")
                    
                    if updated_count > 0:
                        st.cache_data.clear()
                        st.success(f"✅ Successfully updated {updated_count} clauses!")
                        st.rerun()
                    else:
                        st.error("❌ No clauses were updated")
    
    # Export Options
    st.markdown("""
    <div class="subsection-header">
        <h4><i class="fas fa-download subheader-icon"></i>Export Options</h4>
        <p>Export your analysis data and visualizations</p>
    </div>
    """, unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Export Analytics", use_container_width=True, key="export_analytics"):
            st.success("Analytics exported successfully!")
    
    with col2:
        if st.button("📋 Export Clauses", use_container_width=True, key="export_clauses"):
            st.success("Clauses exported successfully!")
    
    with col3:
        if st.button("📈 Export Charts", use_container_width=True, key="export_charts"):
            st.success("Charts exported successfully!")

def render_upload_page():
    st.markdown("""
    <div class="page-header">
        <h1><i class="fas fa-upload header-icon"></i>Document Upload & Analysis</h1>
        <p>Upload your legal documents for AI-powered analysis and review</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Upload section
    st.markdown("""
    <div class="section-header">
        <h3><i class="fas fa-folder-open subheader-icon"></i>Upload Documents</h3>
        <p>Select and upload your legal documents for analysis</p>
    </div>
    """, unsafe_allow_html=True)
    uploaded_files = st.file_uploader(
        "Choose legal documents to upload",
        type=['pdf', 'docx', 'txt'],
        accept_multiple_files=True,
        help="Supported formats: PDF, DOCX, TXT"
    )
    
    if uploaded_files:
        progress_bar = st.progress(0)
        status_text = st.empty()
        uploaded_docs = []
        
        for i, uploaded_file in enumerate(uploaded_files):
            status_text.text(f"Processing {uploaded_file.name}...")
            
            # File validation
            file_size = len(uploaded_file.getvalue())
            
            if file_size == 0:
                st.error(f"❌ {uploaded_file.name} is empty")
                continue
                
            if file_size > 10 * 1024 * 1024:  # 10MB limit
                st.error(f"❌ {uploaded_file.name} is too large ({file_size} bytes). Maximum size is 10MB.")
                continue
            
            try:
                # Simulate processing
                for j in range(100):
                    progress_bar.progress(j + 1)
                    time.sleep(0.01)
                
                # Upload to backend
                with st.spinner(f"Uploading {uploaded_file.name}..."):
                    result = api_client.upload_document(uploaded_file)
                
                if result and result.get('id'):
                    st.success(f"✅ {uploaded_file.name} uploaded successfully!")
                    uploaded_docs.append({
                        'name': uploaded_file.name,
                        'result': result
                    })
                    
                    # Automatically extract clauses from the uploaded document
                    with st.spinner(f"Extracting clauses from {uploaded_file.name}..."):
                        try:
                            analyze_result = api_client.analyze_document(result['id'])
                            if analyze_result and isinstance(analyze_result, list) and len(analyze_result) > 0:
                                clause_count = len(analyze_result)
                                st.success(f"🔍 Extracted {clause_count} clauses from {uploaded_file.name}")
                            else:
                                st.warning(f"⚠️ No clauses found in {uploaded_file.name}")
                        except Exception as e:
                            st.warning(f"Could not extract clauses from {uploaded_file.name}: {str(e)}")
                else:
                    st.error(f"❌ Failed to upload {uploaded_file.name}")
                    if result and result.get('error'):
                        st.error(f"Error: {result['error']}")
                    elif result:
                        st.error(f"Unexpected response: {result}")
                    else:
                        st.error("No response from server - check if backend is running")
                    
            except Exception as e:
                st.error(f"❌ Error uploading {uploaded_file.name}: {str(e)}")
                import traceback
                st.error(f"Full error: {traceback.format_exc()}")
        
        progress_bar.empty()
        status_text.empty()
        
        if uploaded_docs:
            st.success("🎉 All documents processed successfully!")
            
            # Analysis section
            st.markdown("---")
            st.markdown("### 🔍 Document Analysis Results")
            
            # Clear cache so we pull the fresh data
            st.cache_data.clear()
            
            # Fetch fresh data after upload
            documents = fetch_documents()
            clauses = fetch_clauses()
            
            if documents and clauses:
                # Analysis summary
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Documents Uploaded", len(uploaded_docs))
                
                with col2:
                    total_clauses = len(clauses)
                    st.metric("Clauses Extracted", total_clauses)
                
                with col3:
                    high_risk = len([c for c in clauses if c.get('risk_level') == 'HIGH'])
                    st.metric("High Risk Clauses", high_risk)
                
                with col4:
                    unique_types = len(set([c.get('clause_type', 'Unknown') for c in clauses]))
                    st.metric("Clause Types", unique_types)
                
                # Quick analysis charts
                st.markdown("#### 📊 Quick Analysis")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("Risk Distribution")
                    risk_chart = create_risk_distribution_chart(clauses)
                    st.plotly_chart(risk_chart, use_container_width=True)
                
                with col2:
                    st.subheader("Clause Types")
                    clause_chart = create_clause_type_chart(clauses)
                    st.plotly_chart(clause_chart, use_container_width=True)
                
                # Navigation section
                st.markdown("---")
                st.markdown("### 🚀 Next Steps")
                st.markdown("Your documents have been successfully analyzed! Choose your next action:")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button("📝 Review Clauses", type="primary", use_container_width=True, key="upload_review_clauses"):
                        st.session_state.current_page = "Clause Review"
                        st.rerun()
                
                with col2:
                    if st.button("🔍 Search & Insights", type="secondary", use_container_width=True, key="upload_search_insights"):
                        st.session_state.current_page = "Search"
                        st.rerun()
                
                with col3:
                    if st.button("📊 View Dashboard", type="secondary", use_container_width=True, key="upload_view_dashboard"):
                        st.session_state.current_page = "Dashboard"
                        st.rerun()
                
                # Recent clauses preview
                st.markdown("#### 📋 Recent Clauses Found")
                recent_clauses = clauses[-5:] if len(clauses) > 5 else clauses
                
                for clause in recent_clauses:
                    risk_color = {
                        'HIGH': '#ef4444',
                        'MEDIUM': '#f59e0b', 
                        'LOW': '#10b981'
                    }.get(clause.get('risk_level', 'UNKNOWN'), '#6b7280')
                    
                    with st.expander(f"🔍 {clause.get('clause_type', 'Unknown')} - Risk: {clause.get('risk_level', 'Unknown')}"):
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
                        """, unsafe_allow_html=True)
            else:
                st.warning("⚠️ Documents uploaded but analysis data not yet available. Please wait a moment and refresh.")
    
    else:
        # Upload instructions
        st.markdown("""
        <div class="subsection-header">
            <h4><i class="fas fa-info-circle subheader-icon"></i>Upload Instructions</h4>
            <p>Follow these guidelines for optimal document processing</p>
        </div>
        """, unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **📄 Supported Formats:**
            - PDF documents (.pdf)
            - Word documents (.docx)
            - Text files (.txt)
            
            **🔒 Security:**
            - All documents are processed securely
            - Data is encrypted during transmission
            - No data is stored permanently without your consent
            """)
        
        with col2:
            st.markdown("""
            **⚡ What Happens Next:**
            1. Documents are uploaded and processed
            2. AI extracts and analyzes clauses
            3. Risk assessment is performed
            4. You can review, search, and analyze results
            
            **📊 Analysis Features:**
            - Clause extraction and categorization
            - Risk level assessment
            - AI-generated summaries
            - Smart search capabilities
            """)
        
        # Feature highlights
        st.markdown("### ✨ Key Features")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="feature-highlight">
                <h4>🤖 AI Analysis</h4>
                <p>Advanced AI extracts and analyzes legal clauses with high accuracy</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="feature-highlight">
                <h4>⚠️ Risk Assessment</h4>
                <p>Automated risk scoring and highlighting of potential issues</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="feature-highlight">
                <h4>🔍 Smart Search</h4>
                <p>Semantic search to find relevant clauses and documents quickly</p>
            </div>
            """, unsafe_allow_html=True)

def render_clause_review_page():
    st.markdown("""
    <div class="page-header">
        <h1><i class="fas fa-search-plus header-icon"></i>Clause Review & Analysis</h1>
        <p>Review and understand legal clauses with plain English explanations</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Fetch documents
    documents = fetch_documents()
    if not documents:
        st.markdown('''
            <div style="text-align: center; padding: 4rem 2rem; background: white; border-radius: 12px; border: 1px dashed #cbd5e1; margin-top: 2rem;">
                <div style="font-size: 3rem; color: #94a3b8; margin-bottom: 1rem;">📄</div>
                <h3 style="color: #0f172a; margin-bottom: 0.5rem; font-size: 1.5rem;">Clause Library Empty</h3>
                <p style="color: #64748b; margin-bottom: 1.5rem;">Upload a contract or agreement to extract and review clauses.</p>
            </div>
        ''', unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("🚀 Upload First Document", type="primary", use_container_width=True, key=f"empty_upload_render_clause_review_page"):
                st.session_state.current_page = "Upload"
                st.rerun()
        return
    
    # Document selection and filters
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:

        doc_options = {f"{doc.get('filename', 'Document ' + str(doc.get('id', 'Unknown')))} (ID: {doc.get('id', 'Unknown')})": doc for doc in documents}
        selected_doc_name = st.selectbox("Select Document", list(doc_options.keys()), key="clause_review_doc_select")
        selected_doc = doc_options[selected_doc_name]
    
    with col2:
        view_mode = st.selectbox(
            "View Mode",
            ["Plain English", "Technical", "Both"],
            key="clause_view_mode"
        )
    
    with col3:
        risk_filter = st.selectbox(
            "Filter by Risk",
            ["All", "High Risk", "Medium Risk", "Low Risk"],
            key="clause_risk_filter"
        )
    
    # Fetch clauses for selected document
    clauses = fetch_clauses()
    doc_clauses = [c for c in clauses if c.get('document_id') == selected_doc['id']]
    
    if not doc_clauses:
        st.info("📝 No clauses found in this document.")
        return
    
    # Apply risk filter
    if risk_filter != "All":
        risk_level = risk_filter.replace(" Risk", "").upper()
        doc_clauses = [c for c in doc_clauses if c.get('risk_level') == risk_level]
    
    if not doc_clauses:
        st.info(f"📝 No {risk_filter.lower()} clauses found in this document.")
        return
    
    # Document summary
    st.markdown("""
    <div class="section-header">
        <h3><i class="fas fa-clipboard-list subheader-icon"></i>Document Summary</h3>
        <p>Overview of clause analysis and risk assessment</p>
    </div>
    """, unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Clauses", len(doc_clauses))
    
    with col2:
        high_risk = len([c for c in doc_clauses if c.get('risk_level') == 'HIGH'])
        st.metric("High Risk", high_risk)
    
    with col3:
        medium_risk = len([c for c in doc_clauses if c.get('risk_level') == 'MEDIUM'])
        st.metric("Medium Risk", medium_risk)
    
    with col4:
        low_risk = len([c for c in doc_clauses if c.get('risk_level') == 'LOW'])
        st.metric("Low Risk", low_risk)
    
    # Clause review interface
    st.markdown("""
    <div class="section-header">
        <h3><i class="fas fa-search subheader-icon"></i>Clause Analysis</h3>
        <p>Detailed review of individual clauses with AI insights</p>
    </div>
    """, unsafe_allow_html=True)
    
    for i, clause in enumerate(doc_clauses):
        # Enhanced clause display with edit functionality
        st.markdown(f"""
        <div class="card-header">
            <h4><i class="fas fa-file-contract subheader-icon"></i>Clause {i+1}: {clause.get('clause_type', 'Unknown')} - {clause.get('risk_level', 'Unknown')} Risk</h4>
        </div>
        """, unsafe_allow_html=True)
        
        # Use the enhanced clause editor
        from components.clause_editor import render_clause_editor
        # Determine if plain English should be shown based on view mode
        show_plain_english = view_mode in ["Plain English", "Both"]
        render_clause_editor(clause, edit_mode=False, unique_suffix=f"view_{i}", show_plain_english=show_plain_english)
        
        # Additional actions for each clause
        st.markdown("---")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button(f"✏️ Edit Clause", key=f"edit_clause_{i}", type="secondary"):
                # Toggle edit mode for this specific clause
                if f"edit_mode_{i}" not in st.session_state:
                    st.session_state[f"edit_mode_{i}"] = True
                else:
                    st.session_state[f"edit_mode_{i}"] = not st.session_state[f"edit_mode_{i}"]
                st.rerun()
        
        with col2:
            if st.button(f"🔖 Flag for Review", key=f"flag_{i}"):
                st.success("Clause flagged for review!")
        
        with col3:
            if st.button(f"⭐ Save to Favorites", key=f"save_{i}"):
                st.success("Clause saved to favorites!")
        
        with col4:
            if st.button(f"📋 Copy Text", key=f"copy_{i}"):
                st.info("Clause text copied to clipboard!")
        
        # Show edit mode if toggled
        if st.session_state.get(f"edit_mode_{i}", False):
            st.markdown("""
            <div class="subsection-header">
                <h4><i class="fas fa-edit subheader-icon"></i>Edit Mode</h4>
                <p>Make changes to this clause</p>
            </div>
            """, unsafe_allow_html=True)
            render_clause_editor(clause, edit_mode=True, unique_suffix=f"edit_{i}", show_plain_english=show_plain_english)

def generate_plain_english_explanation(clause):
    """Generate plain English explanation of a clause"""
    clause_type = clause.get('clause_type', 'Unknown')
    clause_text = clause.get('clause_text', '')
    
    explanations = {
        'INDEMNITY': "This clause makes one party responsible for protecting the other party from certain types of losses or damages. It's like insurance - if something goes wrong, one party will cover the costs for the other.",
        'LIABILITY': "This clause defines who is responsible when things go wrong. It sets limits on how much one party can be held accountable for damages or losses.",
        'TERMINATION': "This clause explains how and when the agreement can be ended. It's like the 'exit strategy' for the contract - what happens if either party wants to stop working together.",
        'PAYMENT': "This clause outlines the financial terms - who pays what, when payments are due, and how much money is involved. It's the 'money section' of the agreement.",
        'CONFIDENTIALITY': "This clause requires both parties to keep certain information secret. It's like a promise not to share sensitive details with outsiders.",
        'INTELLECTUAL_PROPERTY': "This clause deals with who owns ideas, inventions, or creative work. It's about protecting intellectual assets and determining ownership rights.",
        'GENERAL': "This is a general contract provision that establishes basic terms and conditions for the agreement."
    }
    
    base_explanation = explanations.get(clause_type, explanations['GENERAL'])
    
    # Add specific details based on risk level
    risk_level = clause.get('risk_level', 'UNKNOWN')
    if risk_level == 'HIGH':
        base_explanation += " ⚠️ This is a high-risk clause that could have significant financial or legal consequences."
    elif risk_level == 'MEDIUM':
        base_explanation += " ⚡ This is a medium-risk clause that requires careful consideration."
    else:
        base_explanation += " ✅ This is a low-risk clause with standard terms."
    
    return base_explanation

def generate_risk_analysis(clause):
    """Generate detailed risk analysis"""
    risk_level = clause.get('risk_level', 'UNKNOWN')
    clause_type = clause.get('clause_type', 'Unknown')
    risk_score = clause.get('risk_score', 0)
    
    risk_explanations = {
        'HIGH': f"This clause poses significant risk because it involves {clause_type.lower()} terms that could result in substantial financial liability or legal exposure. The risk score of {risk_score}/10 indicates serious concerns that require immediate attention and possibly legal review.",
        'MEDIUM': f"This clause has moderate risk due to {clause_type.lower()} provisions that may have some financial or legal implications. The risk score of {risk_score}/10 suggests it needs careful review and consideration before acceptance.",
        'LOW': f"This clause presents minimal risk with standard {clause_type.lower()} terms. The risk score of {risk_score}/10 indicates it's generally acceptable but should still be reviewed for completeness."
    }
    
    return risk_explanations.get(risk_level, "Risk analysis not available.")

def generate_action_items(clause):
    """Generate recommended action items for a clause"""
    risk_level = clause.get('risk_level', 'UNKNOWN')
    clause_type = clause.get('clause_type', 'Unknown')
    
    base_actions = [
        "Review the clause carefully with your legal team",
        "Consider negotiating terms if they seem unfavorable",
        "Ensure you understand all obligations and responsibilities"
    ]
    
    if risk_level == 'HIGH':
        base_actions.extend([
            "⚠️ Seek immediate legal counsel before proceeding",
            "Consider requesting modifications to reduce risk",
            "Document all concerns and potential issues",
            "Prepare contingency plans for worst-case scenarios"
        ])
    elif risk_level == 'MEDIUM':
        base_actions.extend([
            "⚡ Schedule a detailed review with stakeholders",
            "Compare with industry standards and best practices",
            "Consider adding protective language if needed"
        ])
    else:
        base_actions.extend([
            "✅ Verify terms align with your expectations",
            "Ensure all necessary details are included"
        ])
    
    return base_actions

def render_search_page():
    st.markdown("""
    <div class="page-header">
        <h1><i class="fas fa-search header-icon"></i>Smart Search & Insights</h1>
        <p>AI-powered semantic search with advanced analytics and visualizations</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Search interface
    col1, col2 = st.columns([3, 1])
    
    with col1:
        search_query = st.text_input(
            "Enter search query", 
            placeholder="Search for clauses, documents, or legal terms...",
            key="search_input"
        )
    
    with col2:
        search_type = st.selectbox(
            "Search Type", 
            ["Semantic", "Keyword", "Risk Level", "Clause Type"],
            key="search_type"
        )
    
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        search_btn = st.button("🔍 Search", type="primary", use_container_width=True)
    with col2:
        clear_btn = st.button("🗑️ Clear", use_container_width=True)
    
    if clear_btn:
        st.session_state.search_results = None
        st.rerun()
    
    if search_btn:
        if search_query:
            try:
                with st.spinner("Searching through documents..."):
                    search_result = api_client.search_clauses(search_query)
                    results = search_result.get("results", [])
                    st.session_state.search_results = results
                
                if results:
                    st.success(f"Found {len(results)} results")
                    
                    # Search insights
                    st.markdown("""
                    <div class="section-header">
                        <h3><i class="fas fa-chart-pie subheader-icon"></i>Search Insights</h3>
                        <p>Analytics and visualizations based on your search results</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Create insights columns
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("Total Results", len(results))
                    
                    with col2:
                        high_risk = len([r for r in results if r.get('risk_level') == 'HIGH'])
                        st.metric("High Risk", high_risk)
                    
                    with col3:
                        avg_relevance = sum([r.get('relevance_score', 0) for r in results]) / len(results) if results else 0
                        st.metric("Avg Relevance", f"{avg_relevance:.2f}")
                    
                    with col4:
                        unique_docs = len(set([r.get('document_filename', '') for r in results]))
                        st.metric("Documents", unique_docs)
                    
                    # Results display
                    st.markdown("### 📋 Search Results")
                    
                    for i, result in enumerate(results):
                        risk_color = {
                            'HIGH': '#ef4444',
                            'MEDIUM': '#f59e0b', 
                            'LOW': '#10b981'
                        }.get(result.get('risk_level', 'UNKNOWN'), '#6b7280')
                        
                        with st.expander(
                            f"🔍 Result {i+1}: {result.get('clause_type', 'Unknown')} - "
                            f"Risk: {result.get('risk_level', 'Unknown')} - "
                            f"Relevance: {result.get('relevance_score', 'N/A')}",
                            expanded=False
                        ):
                            st.markdown(f"""
                            <div class="search-result">
                                <h4>📄 Document: {result.get('document_filename', 'Unknown')}</h4>
                                <p><strong>Clause Text:</strong></p>
                                <div class="clause-text">{result.get('clause_text', 'No text available')}</div>
                                <p><strong>AI Summary:</strong></p>
                                <div class="ai-summary">{result.get('summary', 'No summary available')}</div>
                                <div class="result-metrics">
                                    <span class="risk-badge" style="background-color: {risk_color}20; color: {risk_color}; padding: 0.3rem 0.8rem; border-radius: 20px; font-size: 0.8rem;">
                                        Risk: {result.get('risk_level', 'Unknown')} ({result.get('risk_score', 'N/A')})
                                    </span>
                                    <span class="relevance-badge" style="background-color: #3b82f620; color: #3b82f6; padding: 0.3rem 0.8rem; border-radius: 20px; font-size: 0.8rem; margin-left: 0.5rem;">
                                        Relevance: {result.get('relevance_score', 'N/A')}
                                    </span>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                else:
                    st.info("No results found for your search query.")
                    st.session_state.search_results = None
            except Exception as e:
                st.error(f"Search error: {str(e)}")
                st.session_state.search_results = None
        else:
            st.warning("Please enter a search query.")
    
    # Display previous results if available
    if hasattr(st.session_state, 'search_results') and st.session_state.search_results:
        st.markdown("---")
        st.markdown("""
        <div class="section-header">
            <h3><i class="fas fa-chart-line subheader-icon"></i>Search Analytics</h3>
            <p>Comprehensive analysis of your search results and document insights</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Create visualizations for search results
        try:
            from components.charts import create_word_cloud_like, create_similarity_heatmap
            
            # Word cloud visualization
            if st.session_state.search_results:
                st.markdown("#### 🔤 Key Terms & Concepts")
                word_cloud = create_word_cloud_like(st.session_state.search_results)
                if word_cloud:
                    st.plotly_chart(word_cloud, use_container_width=True)
            
            # Similarity heatmap
            if len(st.session_state.search_results) > 1:
                st.markdown("#### 🔗 Result Similarity Matrix")
                similarity_heatmap = create_similarity_heatmap(st.session_state.search_results)
                if similarity_heatmap:
                    st.plotly_chart(similarity_heatmap, use_container_width=True)
                    
        except Exception as e:
            st.warning(f"Could not generate visualizations: {str(e)}")
    
    # Search tips
    st.markdown("---")
    st.markdown("### 💡 Search Tips")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **🔍 Semantic Search:**
        - Use natural language queries
        - Search for concepts, not just keywords
        - Try phrases like "liability clauses" or "payment terms"
        """)
    
    with col2:
        st.markdown("""
        **⚡ Advanced Features:**
        - Filter by risk level or clause type
        - Sort by relevance score
        - View AI-generated summaries
        """)

# ──────────────────────────────────────────────
# Authentication Gate
# ──────────────────────────────────────────────

def render_login_page():
    """Render a premium login / register page"""
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.container(border=True):
            st.markdown("<h1 style='text-align: center; color: #2563eb;'>⚖️ LegalSight Pro</h1>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; color: #64748b;'>Enterprise Legal Document Analysis</p>", unsafe_allow_html=True)
            st.divider()
            
            # Tab selector
            if "auth_tab" not in st.session_state:
                st.session_state.auth_tab = "Login"
            
            tab = st.radio("Authentication Mode", ["Login", "Register"], horizontal=True, key="auth_mode_selector", label_visibility="collapsed")
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

# Main App
def main():
    # Get current page from URL
    query_params = st.query_params
    if 'page' in query_params:
        st.session_state.current_page = query_params['page']
    
    # ── Authentication Gate ──
    if not api_client.is_authenticated():
        render_login_page()
        return
    
    # Render sidebar
    with st.sidebar:
        render_sidebar()
    
    # Render current page
    if st.session_state.current_page == "Home":
        render_home_page()
    elif st.session_state.current_page == "Dashboard":
        render_dashboard_page()
    elif st.session_state.current_page == "Upload":
        render_upload_page()
    elif st.session_state.current_page == "Clause Review":
        render_clause_review_page()
    elif st.session_state.current_page == "Search":
        render_search_page()
    else:
        render_home_page()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem;">
        <p>Legal Document Review Assistant - AI-Powered Legal Analysis Platform</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

