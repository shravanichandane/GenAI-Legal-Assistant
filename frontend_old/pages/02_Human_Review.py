import streamlit as st
import sys
import os

# Add the project root to sys.path to import app modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from app.review.workflow import ReviewWorkflow, ReviewStatus
from app.review.audit_logger import AuditLogger

st.set_page_config(page_title="Human Review Workflow", layout="wide")

st.title("Human-in-the-Loop Review Dashboard")
st.markdown("Review AI-generated risk reports, assess evidence, and provide final decisions.")

# Initialize Audit Logger
# Store the log file in the data directory
DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data'))
os.makedirs(DATA_DIR, exist_ok=True)
LOG_FILE = os.path.join(DATA_DIR, "audit_log.jsonl")
audit_logger = AuditLogger(log_file_path=LOG_FILE)

# Mock Data (Simulating Week 7 Output)
MOCK_REPORT = {
    "document_id": "DOC-2026-0812",
    "title": "Vendor Master Services Agreement",
    "risk_score": 8.5,
    "risk_level": "High",
    "llm_recommendation": "Reject due to unlimited liability clause and unfavorable termination terms.",
    "evidence": [
        "Clause 4.2 states liability is uncapped for both parties.",
        "Clause 9.1 allows termination for convenience with only 5 days notice."
    ],
    "precedents": [
        "In similar agreements (e.g., DOC-2025-0199), liability was capped at 2x contract value.",
        "Standard termination notice period in past approved contracts is 30 days."
    ]
}

# Initialize session state for workflow
if "workflow" not in st.session_state:
    st.session_state.workflow = ReviewWorkflow(document_id=MOCK_REPORT["document_id"])
if "reviewer_id" not in st.session_state:
    st.session_state.reviewer_id = "Reviewer_Alice_01"
if "review_complete" not in st.session_state:
    st.session_state.review_complete = False

# Display Document Info
st.header(f"Document: {MOCK_REPORT['title']}")
col1, col2 = st.columns(2)
with col1:
    st.write(f"**Document ID:** {MOCK_REPORT['document_id']}")
    st.write(f"**Current Status:** `{st.session_state.workflow.get_status()}`")
with col2:
    st.write(f"**Reviewer ID:** `{st.session_state.reviewer_id}`")
    risk_color = "red" if MOCK_REPORT["risk_score"] > 7 else "orange" if MOCK_REPORT["risk_score"] > 4 else "green"
    st.markdown(f"**AI Risk Score:** <span style='color:{risk_color}'>{MOCK_REPORT['risk_score']} ({MOCK_REPORT['risk_level']})</span>", unsafe_allow_html=True)

st.divider()

# Side-by-side Evidence, Precedents, and Recommendation
st.subheader("AI Analysis & Context")
ev_col, pre_col, rec_col = st.columns(3)

with ev_col:
    st.markdown("### 📝 Extracted Evidence")
    for item in MOCK_REPORT["evidence"]:
        st.info(item)

with pre_col:
    st.markdown("### 📚 Historical Precedents")
    for item in MOCK_REPORT["precedents"]:
        st.warning(item)

with rec_col:
    st.markdown("### 🤖 LLM Recommendation")
    st.error(MOCK_REPORT["llm_recommendation"])

st.divider()

# Action Area
st.subheader("Final Decision")
reviewer_comments = st.text_area("Reviewer Comments (Optional)", help="Add any notes regarding your decision.")

if st.session_state.review_complete:
    st.success(f"Review completed. Final Status: {st.session_state.workflow.get_status()}")
    if st.button("Review Another Document (Reset)"):
        st.session_state.workflow = ReviewWorkflow(document_id=MOCK_REPORT["document_id"])
        st.session_state.review_complete = False
        st.rerun()
else:
    btn_col1, btn_col2, btn_col3 = st.columns(3)
    
    def process_decision(action: ReviewStatus):
        # Update workflow
        st.session_state.workflow.transition_to(action)
        # Log to audit
        audit_logger.log_action(
            reviewer_id=st.session_state.reviewer_id,
            document_id=MOCK_REPORT["document_id"],
            original_risk_score=MOCK_REPORT["risk_score"],
            action_taken=action.value,
            comments=reviewer_comments
        )
        st.session_state.review_complete = True
        
    with btn_col1:
        if st.button("✅ Approve", use_container_width=True, type="primary"):
            process_decision(ReviewStatus.APPROVED)
            st.rerun()
            
    with btn_col2:
        if st.button("❌ Reject", use_container_width=True, type="primary"):
            process_decision(ReviewStatus.REJECTED)
            st.rerun()
            
    with btn_col3:
        if st.button("✏️ Modify", use_container_width=True, type="secondary"):
            process_decision(ReviewStatus.MODIFIED)
            st.rerun()

# Display Recent Audit Logs
with st.expander("View Recent Audit Logs"):
    logs = audit_logger.get_logs()
    if logs:
        st.dataframe(logs[-5:])
    else:
        st.write("No logs available.")
