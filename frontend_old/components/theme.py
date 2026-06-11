### frontend/components/theme.py

import streamlit as st

def apply_elite_theme():
    st.markdown("""
        <style>
        /* Global Typography & Colors */
        :root {
            --primary: #1E3A8A; /* Deep Navy */
            --secondary: #334155; /* Slate Gray */
            --bg-off-white: #F8FAFC;
            --accent-warning: #D97706; /* Soft Amber */
            --accent-critical: #DC2626; /* Light Crimson */
        }
        
        /* Elite Feature Cards */
        .elite-card {
            background-color: white;
            border: 1px solid #E2E8F0;
            border-radius: 12px;
            padding: 1.5rem;
            height: 100%;
            transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out, border-color 0.2s ease-in-out;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        }
        .elite-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
            border-color: #1E3A8A;
        }
        
        /* Premium Buttons */
        .stButton > button {
            transition: all 0.3s ease !important;
            border-radius: 8px !important;
            font-weight: 600 !important;
        }
        
        /* File Uploader Premium Area */
        [data-testid="stFileUploader"] {
            padding: 2rem !important;
            border: 2px dashed #CBD5E1 !important;
            border-radius: 16px !important;
            background-color: #F8FAFC !important;
            transition: all 0.3s ease !important;
        }
        [data-testid="stFileUploader"]:hover {
            border-color: #1E3A8A !important;
            background-color: #F1F5F9 !important;
        }
        
        /* Legal Serif Typography for Clauses */
        .legal-serif {
            font-family: 'Georgia', 'Merriweather', serif;
            color: #334155;
            font-size: 1.05rem;
            line-height: 1.7;
            background: #F8FAFC;
            padding: 1.5rem;
            border-left: 4px solid #1E3A8A;
            border-radius: 0 8px 8px 0;
            margin-top: 0.5rem;
        }
        
        /* KPI Metrics Elite Card */
        .kpi-card {
            background-color: white;
            border: 1px solid #E2E8F0;
            border-radius: 12px;
            padding: 1.5rem;
            text-align: center;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        }
        .kpi-label {
            color: #64748b;
            font-weight: 600;
            text-transform: uppercase;
            font-size: 0.85rem;
            letter-spacing: 0.05em;
            margin-bottom: 0.5rem;
        }
        .kpi-value {
            color: #1E3A8A;
            font-size: 2.5rem;
            font-weight: 700;
            line-height: 1.2;
        }
        
        </style>
    """, unsafe_allow_html=True)
