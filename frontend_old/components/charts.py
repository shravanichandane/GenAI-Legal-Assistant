### frontend/components/charts.py

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import streamlit as st
import numpy as np

# Professional color palette
PROFESSIONAL_COLORS = {
    'primary': '#3b82f6',
    'secondary': '#8b5cf6', 
    'accent': '#06b6d4',
    'success': '#10b981',
    'warning': '#f59e0b',
    'danger': '#ef4444',
    'muted': '#64748b'
}

RISK_COLORS = {
    'LOW': '#10b981',
    'MEDIUM': '#f59e0b', 
    'HIGH': '#ef4444'
}

def create_professional_theme():
    """Create consistent professional theme for all charts"""
    return {
        'layout': {
            'font': {'family': 'Inter, sans-serif', 'size': 12, 'color': '#334155'},
            'plot_bgcolor': 'rgba(0,0,0,0)',
            'paper_bgcolor': 'rgba(0,0,0,0)',
            'colorway': [PROFESSIONAL_COLORS['primary'], PROFESSIONAL_COLORS['secondary'], 
                        PROFESSIONAL_COLORS['accent'], PROFESSIONAL_COLORS['success'], 
                        PROFESSIONAL_COLORS['warning'], PROFESSIONAL_COLORS['danger']],
            'margin': dict(l=20, r=20, t=60, b=40),
        }
    }

def create_clause_type_chart(clause_data):
    """Create clause type distribution chart"""
    if not clause_data:
        # Return empty chart with helpful message
        fig = go.Figure()
        fig.add_annotation(
            text="No clause data available<br><span style='font-size: 12px; color: #94a3b8;'>Upload and analyze documents to see distribution</span>",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(size=16, color="#64748b"),
            align="center"
        )
        fig.update_layout(
            title={
                'text': "Clause Type Distribution",
                'x': 0.5,
                'font': {'size': 18, 'color': '#1e293b', 'family': 'Inter, sans-serif'}
            },
            height=400,
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            **create_professional_theme()['layout']
        )
        return fig
    
    # Process clause data - count clause types
    clause_types = {}
    for clause in clause_data:
        clause_type = clause.get('clause_type', 'Unknown')
        clause_types[clause_type] = clause_types.get(clause_type, 0) + 1
    
    if not clause_types:
        # Return empty chart with helpful message
        fig = go.Figure()
        fig.add_annotation(
            text="No clause data available<br><span style='font-size: 12px; color: #94a3b8;'>Upload and analyze documents to see distribution</span>",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(size=16, color="#64748b"),
            align="center"
        )
        fig.update_layout(
            title={
                'text': "Clause Type Distribution",
                'x': 0.5,
                'font': {'size': 18, 'color': '#1e293b', 'family': 'Inter, sans-serif'}
            },
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            **create_professional_theme()['layout']
        )
        return fig
    
    df = pd.DataFrame(list(clause_types.items()), columns=['Clause Type', 'Count'])
    
    # Donut chart with professional styling
    fig = go.Figure(data=[go.Pie(
        labels=df['Clause Type'], 
        values=df['Count'],
        hole=0.4,
        marker=dict(
            colors=[PROFESSIONAL_COLORS['primary'], PROFESSIONAL_COLORS['secondary'], 
                   PROFESSIONAL_COLORS['accent'], PROFESSIONAL_COLORS['success'],
                   PROFESSIONAL_COLORS['warning'], PROFESSIONAL_COLORS['danger']],
            line=dict(color='white', width=2)
        ),
        textinfo='label+percent',
        textposition='outside',
        textfont=dict(size=11, color='#334155'),
        hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
    )])

    fig.update_layout(
        title={
            'text': "Clause Type Distribution",
            'x': 0.5,
            'font': {'size': 18, 'color': '#1e293b', 'family': 'Inter, sans-serif'}
        },
        height=400,
        showlegend=True,
        legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1.05, font=dict(size=10, color='#475569')),
        **create_professional_theme()['layout']
    )
    
    return fig

def create_risk_distribution_chart(risk_data):
    """Create risk level distribution chart"""
    if not risk_data:
        # Return empty chart with helpful message
        fig = go.Figure()
        fig.add_annotation(
            text="No risk data available<br><span style='font-size: 12px; color: #94a3b8;'>Upload and analyze documents to see risk distribution</span>",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(size=16, color="#64748b"),
            align="center"
        )
        fig.update_layout(
            title={
                'text': "Risk Level Distribution",
                'x': 0.5,
                'font': {'size': 18, 'color': '#1e293b', 'family': 'Inter, sans-serif'}
            },
            height=400,
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            **create_professional_theme()['layout']
        )
        return fig
    
    # Process risk data - count risk levels
    risk_levels = {}
    for clause in risk_data:
        risk_level = clause.get('risk_level', 'Unknown')
        risk_levels[risk_level] = risk_levels.get(risk_level, 0) + 1
    
    if not risk_levels:
        # Return empty chart with helpful message
        fig = go.Figure()
        fig.add_annotation(
            text="No risk data available<br><span style='font-size: 12px; color: #94a3b8;'>Upload and analyze documents to see risk distribution</span>",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(size=16, color="#64748b"),
            align="center"
        )
        fig.update_layout(
            title={
                'text': "Risk Level Distribution",
                'x': 0.5,
                'font': {'size': 18, 'color': '#1e293b', 'family': 'Inter, sans-serif'}
            },
            height=400,
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            **create_professional_theme()['layout']
        )
        return fig
    
    fig = go.Figure()
    for risk_level, count in risk_levels.items():
        fig.add_trace(go.Bar(
            x=[risk_level],
            y=[count],
            name=risk_level,
            marker=dict(color=RISK_COLORS.get(risk_level, PROFESSIONAL_COLORS['muted']), line=dict(color='white', width=1)),
            text=[count],
            textposition='auto',
            textfont=dict(size=12, color='white', weight='bold'),
            hovertemplate=f'<b>{risk_level} Risk</b><br>Count: %{{y}}<extra></extra>'
        ))
    
    fig.update_layout(
        title={
            'text': "Risk Level Distribution",
            'x': 0.5,
            'font': {'size': 18, 'color': '#1e293b', 'family': 'Inter, sans-serif'}
        },
        xaxis=dict(title=dict(text="Risk Level", font=dict(size=14, color='#475569')), tickfont=dict(size=12, color='#64748b'), gridcolor='rgba(148, 163, 184, 0.2)'),
        yaxis=dict(title=dict(text="Number of Clauses", font=dict(size=14, color='#475569')), tickfont=dict(size=12, color='#64748b'), gridcolor='rgba(148, 163, 184, 0.2)'),
        height=400,
        showlegend=False,
        **create_professional_theme()['layout']
    )
    
    return fig

def create_risk_heatmap(clauses_df):
    """Create risk heatmap by clause type"""
    if clauses_df.empty:
        fig = go.Figure()
        fig.add_annotation(
            text="No clause data available<br><span style='font-size: 12px; color: #94a3b8;'>Upload and analyze documents to see risk patterns</span>",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(size=16, color="#64748b"),
            align="center"
        )
        fig.update_layout(
            title={
                'text': "Risk Heatmap by Clause Type",
                'x': 0.5,
                'font': {'size': 18, 'color': '#1e293b', 'family': 'Inter, sans-serif'}
            },
            height=400,
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            **create_professional_theme()['layout']
        )
        return fig
    
    # Group by clause type and risk level
    try:
        heatmap_data = clauses_df.groupby(['clause_type', 'risk_level']).size().unstack(fill_value=0)
        
        if heatmap_data.empty:
            fig = go.Figure()
            fig.add_annotation(text="Insufficient data for heatmap", x=0.5, y=0.5)
            return fig
        
        fig = go.Figure(data=go.Heatmap(
            z=heatmap_data.values,
            x=heatmap_data.columns,
            y=heatmap_data.index,
            colorscale=[[0, '#f1f5f9'], [0.5, '#fbbf24'], [1, '#ef4444']],
            text=heatmap_data.values,
            texttemplate="%{text}",
            textfont={"size": 12, "color": "white"},
            hoverongaps=False,
            hovertemplate='<b>%{y}</b><br>Risk Level: %{x}<br>Count: %{z}<extra></extra>',
            showscale=True,
            colorbar=dict(title="Count", titlefont=dict(size=12, color='#475569'), tickfont=dict(size=10, color='#64748b'))
        ))
        
        fig.update_layout(
            title={
                'text': "Risk Heatmap by Clause Type",
                'x': 0.5,
                'font': {'size': 18, 'color': '#1e293b', 'family': 'Inter, sans-serif'}
            },
            xaxis=dict(title=dict(text="Risk Level", font=dict(size=14, color='#475569')), tickfont=dict(size=12, color='#64748b')),
            yaxis=dict(title=dict(text="Clause Type", font=dict(size=14, color='#475569')), tickfont=dict(size=12, color='#64748b')),
            height=400,
            **create_professional_theme()['layout']
        )
        
        return fig
        
    except Exception as e:
        fig = go.Figure()
        fig.add_annotation(text="Error creating heatmap", x=0.5, y=0.5)
        return fig

def create_kpi_cards(analytics_data):
    """Create enhanced KPI cards with professional styling"""
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="metric-container">
            <div style="color: {PROFESSIONAL_COLORS['primary']}; font-size: 2rem; margin-bottom: 0.5rem;">📄</div>
            <div style="font-size: 2rem; font-weight: 700; color: #1e293b;">{analytics_data.get('total_documents', 0)}</div>
            <div style="color: #64748b; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 0.05em;">Total Documents</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-container">
            <div style="color: {PROFESSIONAL_COLORS['secondary']}; font-size: 2rem; margin-bottom: 0.5rem;">📋</div>
            <div style="font-size: 2rem; font-weight: 700; color: #1e293b;">{analytics_data.get('total_clauses', 0)}</div>
            <div style="color: #64748b; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 0.05em;">Total Clauses</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        high_risk_pct = analytics_data.get('high_risk_percentage', 0)
        risk_color = RISK_COLORS['HIGH'] if high_risk_pct > 20 else RISK_COLORS['MEDIUM'] if high_risk_pct > 10 else RISK_COLORS['LOW']
        st.markdown(f"""
        <div class="metric-container">
            <div style="color: {risk_color}; font-size: 2rem; margin-bottom: 0.5rem;">⚠️</div>
            <div style="font-size: 2rem; font-weight: 700; color: #1e293b;">{high_risk_pct:.1f}%</div>
            <div style="color: #64748b; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 0.05em;">High Risk Clauses</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        avg_score = analytics_data.get('average_risk_score', 0)
        st.markdown(f"""
        <div class="metric-container">
            <div style="color: {PROFESSIONAL_COLORS['accent']}; font-size: 2rem; margin-bottom: 0.5rem;">📊</div>
            <div style="font-size: 2rem; font-weight: 700; color: #1e293b;">{avg_score:.1f}<span style=\"font-size: 1rem; color: #64748b;\">/10</span></div>
            <div style="color: #64748b; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 0.05em;">Average Risk Score</div>
        </div>
        """, unsafe_allow_html=True)

def create_temporal_trend_chart(documents: list):
    """Create temporal trends for uploads and average risk over time"""
    if not documents:
        fig = go.Figure()
        fig.add_annotation(text="No temporal data available", x=0.5, y=0.5, showarrow=False)
        fig.update_layout(height=360, **create_professional_theme()['layout'])
        return fig
    df = pd.DataFrame(documents)
    if 'upload_date' in df.columns:
        df['upload_date'] = pd.to_datetime(df['upload_date'])
        # uploads per day
        uploads = df.groupby(pd.Grouper(key='upload_date', freq='D')).size().rename('uploads').to_frame()
        # optional average risk per day
        if 'average_risk_score' in df.columns:
            avg_risk = df.groupby(pd.Grouper(key='upload_date', freq='D'))['average_risk_score'].mean().rename('average_risk_score')
            daily = uploads.join(avg_risk, how='left')
        else:
            daily = uploads
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Bar(x=daily.index, y=daily['uploads'], name='Uploads', marker_color=PROFESSIONAL_COLORS['primary']), secondary_y=False)
        if 'average_risk_score' in daily.columns:
            fig.add_trace(go.Scatter(x=daily.index, y=daily['average_risk_score'], name='Avg Risk', mode='lines+markers', line=dict(color=PROFESSIONAL_COLORS['danger'])), secondary_y=True)
        fig.update_layout(title={ 'text': 'Temporal Trends', 'x': 0.5 }, height=400, **create_professional_theme()['layout'])
        fig.update_xaxes(title_text='Date')
        fig.update_yaxes(title_text='Uploads', secondary_y=False)
        if 'average_risk_score' in daily.columns:
            fig.update_yaxes(title_text='Avg Risk', secondary_y=True)
        return fig
    else:
        fig = go.Figure()
        fig.add_annotation(text="Missing upload_date in data", x=0.5, y=0.5, showarrow=False)
        return fig

def create_clause_comparison_chart(clauses: list):
    """Compare clause counts by type and risk"""
    if not clauses:
        fig = go.Figure(); fig.add_annotation(text="No clause data", x=0.5, y=0.5, showarrow=False); return fig
    df = pd.DataFrame(clauses)
    if not {'clause_type','risk_level'}.issubset(df.columns):
        fig = go.Figure(); fig.add_annotation(text="Insufficient clause fields", x=0.5, y=0.5, showarrow=False); return fig
    counts = df.groupby(['clause_type','risk_level']).size().reset_index(name='count')
    fig = px.bar(counts, x='clause_type', y='count', color='risk_level', barmode='group', color_discrete_map=RISK_COLORS)
    fig.update_layout(title={ 'text': 'Clause Type vs Risk', 'x': 0.5 }, height=420, **create_professional_theme()['layout'])
    fig.update_xaxes(title_text='Clause Type'); fig.update_yaxes(title_text='Count')
    return fig

def create_similarity_heatmap(similarity_matrix: np.ndarray, labels: list):
    """Visualize similarity matrix between clauses/documents"""
    if similarity_matrix is None or len(similarity_matrix) == 0:
        fig = go.Figure(); fig.add_annotation(text="No similarity data", x=0.5, y=0.5, showarrow=False); return fig
    fig = go.Figure(data=go.Heatmap(z=similarity_matrix, x=labels, y=labels, colorscale='Blues', colorbar=dict(title='Similarity')))
    fig.update_layout(title={ 'text': 'Similarity Heatmap', 'x': 0.5 }, height=420, **create_professional_theme()['layout'])
    return fig

def create_word_cloud_like(results: list):
    """Approximate word cloud using scatter with frequency-based sizes"""
    if not results:
        fig = go.Figure(); fig.add_annotation(text="No terms", x=0.5, y=0.5, showarrow=False); return fig
    # Build term frequencies from summaries/text
    from collections import Counter
    words = []
    for r in results:
        text = (r.get('summary') or '') + ' ' + (r.get('clause_text') or '')
        words.extend([w.lower() for w in text.split() if len(w) > 4])
    freq = Counter(words).most_common(40)
    if not freq:
        fig = go.Figure(); fig.add_annotation(text="No significant terms", x=0.5, y=0.5, showarrow=False); return fig
    terms, counts = zip(*freq)
    x = np.random.rand(len(terms))
    y = np.random.rand(len(terms))
    sizes = np.interp(counts, (min(counts), max(counts)), (12, 36))
    fig = go.Figure(data=go.Scatter(x=x, y=y, mode='text', text=terms, textfont=dict(size=sizes, color=PROFESSIONAL_COLORS['muted'])))
    fig.update_layout(title={ 'text': 'Search Term Highlights', 'x': 0.5 }, xaxis=dict(visible=False), yaxis=dict(visible=False), height=380, **create_professional_theme()['layout'])
    return fig
