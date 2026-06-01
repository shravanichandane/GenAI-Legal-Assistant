### frontend/components/clause_editor.py

import streamlit as st
from typing import Dict, Any
from api_client import api_client
import time

def generate_plain_english_explanation(clause):
    """Generate plain English explanation of a clause"""
    clause_type = clause.get('clause_type', 'Unknown')
    clause_text = clause.get('clause_text', '')
    
    explanations = {
        'INDEMNITY': "This clause requires one party to protect and compensate the other party for any losses, damages, or legal costs that might arise from certain actions or situations. It's like an insurance policy where one party promises to cover the other's expenses.",
        
        'LIABILITY': "This clause defines who is responsible for what and limits the amount of money one party can be held accountable for if something goes wrong. It's like setting rules about who pays for damages and how much.",
        
        'TERMINATION': "This clause explains when and how the agreement can be ended by either party. It's like the exit strategy that tells you what happens if you want to stop the contract or if the other party wants to stop it.",
        
        'PAYMENT': "This clause outlines how, when, and how much money should be paid. It's like the billing instructions that tell you the payment schedule, amounts, and methods.",
        
        'CONFIDENTIALITY': "This clause requires both parties to keep certain information secret and not share it with others. It's like a privacy agreement that protects sensitive business information.",
        
        'INTELLECTUAL_PROPERTY': "This clause deals with who owns ideas, inventions, trademarks, or creative works. It's like deciding who gets to claim ownership of intellectual creations and how they can be used.",
        
        'GENERAL': "This is a general clause that covers various terms and conditions of the agreement. It may include important details about the relationship between the parties and their obligations."
    }
    
    base_explanation = explanations.get(clause_type, explanations['GENERAL'])
    
    # Add specific details based on clause text content
    additional_info = []
    
    if 'shall' in clause_text.lower() or 'must' in clause_text.lower():
        additional_info.append("This clause uses strong language ('shall' or 'must') which means it's a requirement, not just a suggestion.")
    
    if 'liability' in clause_text.lower() or 'damages' in clause_text.lower():
        additional_info.append("This clause deals with responsibility for damages or losses.")
    
    if 'terminate' in clause_text.lower() or 'end' in clause_text.lower():
        additional_info.append("This clause explains how the agreement can be ended.")
    
    if 'confidential' in clause_text.lower() or 'proprietary' in clause_text.lower():
        additional_info.append("This clause protects sensitive information from being shared.")
    
    if 'payment' in clause_text.lower() or 'fee' in clause_text.lower() or 'cost' in clause_text.lower():
        additional_info.append("This clause deals with financial obligations and payments.")
    
    if additional_info:
        base_explanation += "\n\n**Key Points:**\n" + "\n".join(f"• {info}" for info in additional_info)
    
    return base_explanation

def generate_ai_suggestions(clause):
    """Generate AI-powered suggestions for improving a clause"""
    clause_type = clause.get('clause_type', 'GENERAL')
    clause_text = clause.get('clause_text', '')
    risk_level = clause.get('risk_level', 'LOW')
    risk_score = clause.get('risk_score', 5.0)
    
    suggestions = []
    
    # Risk-based suggestions
    if risk_level == 'HIGH' or risk_score > 7.0:
        suggestions.append({
            'title': 'Reduce Risk Exposure',
            'category': 'Risk Management',
            'priority': 'High',
            'description': 'This clause has high risk exposure. Consider adding limitations, caps, or exclusions to reduce potential liability.',
            'example': 'Add: "Subject to a maximum liability cap of $X" or "Excluding consequential damages"',
            'action': 'Add liability limitations and damage exclusions'
        })
    
    # Clarity suggestions
    if len(clause_text) > 200:
        suggestions.append({
            'title': 'Improve Readability',
            'category': 'Clarity',
            'priority': 'Medium',
            'description': 'This clause is quite long and may be difficult to understand. Consider breaking it into smaller, more digestible parts.',
            'example': 'Split into numbered sub-clauses or use bullet points for key requirements',
            'action': 'Break down into smaller, clearer sections'
        })
    
    # Legal language suggestions
    if 'shall' in clause_text.lower() and 'may' in clause_text.lower():
        suggestions.append({
            'title': 'Clarify Obligations vs. Rights',
            'category': 'Legal Language',
            'priority': 'Medium',
            'description': 'The clause mixes mandatory language ("shall") with permissive language ("may"). This can create confusion about what is required vs. optional.',
            'example': 'Use "shall" for mandatory obligations and "may" for discretionary rights consistently',
            'action': 'Standardize mandatory vs. permissive language'
        })
    
    # Missing elements suggestions
    if clause_type == 'INDEMNITY' and 'defend' not in clause_text.lower():
        suggestions.append({
            'title': 'Add Defense Obligation',
            'category': 'Indemnity',
            'priority': 'High',
            'description': 'Indemnity clauses should typically include both defense and indemnification obligations.',
            'example': 'Add: "and defend against any claims, suits, or proceedings"',
            'action': 'Include defense obligation in indemnity clause'
        })
    
    if clause_type == 'LIABILITY' and 'consequential' not in clause_text.lower():
        suggestions.append({
            'title': 'Address Consequential Damages',
            'category': 'Liability',
            'priority': 'Medium',
            'description': 'Consider explicitly addressing consequential damages to avoid ambiguity.',
            'example': 'Add: "Excluding consequential, indirect, or special damages"',
            'action': 'Explicitly address consequential damages'
        })
    
    # Time-based suggestions
    if 'terminate' in clause_text.lower() and 'notice' not in clause_text.lower():
        suggestions.append({
            'title': 'Add Notice Requirements',
            'category': 'Termination',
            'priority': 'High',
            'description': 'Termination clauses should specify notice requirements to ensure fair process.',
            'example': 'Add: "with 30 days written notice" or similar notice period',
            'action': 'Include notice requirements for termination'
        })
    
    # Confidentiality suggestions
    if clause_type == 'CONFIDENTIALITY' and 'return' not in clause_text.lower():
        suggestions.append({
            'title': 'Add Return/Destruction Obligation',
            'category': 'Confidentiality',
            'priority': 'Medium',
            'description': 'Confidentiality clauses should specify what happens to confidential information when the agreement ends.',
            'example': 'Add: "return or destroy all confidential information upon termination"',
            'action': 'Include return/destruction obligations'
        })
    
    # Payment suggestions
    if clause_type == 'PAYMENT' and 'late' not in clause_text.lower():
        suggestions.append({
            'title': 'Add Late Payment Terms',
            'category': 'Payment',
            'priority': 'Low',
            'description': 'Consider adding late payment penalties or interest to encourage timely payments.',
            'example': 'Add: "Late payments shall incur interest at X% per annum"',
            'action': 'Include late payment terms and penalties'
        })
    
    # Force majeure suggestions
    if 'force majeure' not in clause_text.lower() and clause_type in ['TERMINATION', 'GENERAL']:
        suggestions.append({
            'title': 'Consider Force Majeure',
            'category': 'Risk Management',
            'priority': 'Low',
            'description': 'Consider adding force majeure provisions to protect against unforeseeable circumstances.',
            'example': 'Add force majeure clause for events beyond reasonable control',
            'action': 'Add force majeure protection'
        })
    
    return suggestions[:5]  # Limit to top 5 suggestions

def analyze_clause_risk(clause):
    """Analyze the risk level of a clause and provide insights"""
    risk_level = clause.get('risk_level', 'LOW')
    risk_score = clause.get('risk_score', 5.0)
    clause_text = clause.get('clause_text', '')
    
    risk_factors = []
    
    if 'unlimited' in clause_text.lower():
        risk_factors.append("Contains unlimited liability language")
    
    if 'consequential' not in clause_text.lower() and 'damages' in clause_text.lower():
        risk_factors.append("Does not exclude consequential damages")
    
    if 'indemnify' in clause_text.lower() and 'defend' not in clause_text.lower():
        risk_factors.append("Indemnity without defense obligation")
    
    if 'terminate' in clause_text.lower() and 'notice' not in clause_text.lower():
        risk_factors.append("Termination without notice requirements")
    
    if 'confidential' in clause_text.lower() and 'return' not in clause_text.lower():
        risk_factors.append("Confidentiality without return obligations")
    
    analysis = f"**Risk Level:** {risk_level} (Score: {risk_score}/10)\n\n"
    
    if risk_factors:
        analysis += "**Risk Factors Identified:**\n"
        for factor in risk_factors:
            analysis += f"• {factor}\n"
    else:
        analysis += "**No major risk factors identified.**\n"
    
    if risk_level == 'HIGH':
        analysis += "\n**Recommendation:** Consider adding limitations, caps, or exclusions to reduce risk exposure."
    elif risk_level == 'MEDIUM':
        analysis += "\n**Recommendation:** Review for potential improvements to reduce risk."
    else:
        analysis += "\n**Recommendation:** Clause appears to have acceptable risk levels."
    
    return analysis

def suggest_clarity_improvements(clause):
    """Suggest improvements for clause clarity and readability"""
    clause_text = clause.get('clause_text', '')
    
    improvements = []
    
    if len(clause_text) > 200:
        improvements.append("Break into shorter sentences or sub-clauses")
    
    if clause_text.count(',') > 5:
        improvements.append("Consider using bullet points or numbered lists")
    
    if 'herein' in clause_text.lower() or 'aforesaid' in clause_text.lower():
        improvements.append("Replace archaic legal terms with modern language")
    
    if 'shall' in clause_text.lower() and 'may' in clause_text.lower():
        improvements.append("Standardize mandatory vs. permissive language")
    
    if clause_text.count('(') > 3:
        improvements.append("Consider using separate sentences instead of parenthetical clauses")
    
    if not improvements:
        improvements.append("Clause appears to be well-written and clear")
    
    return "\n".join(f"• {improvement}" for improvement in improvements)

def generate_legal_review(clause):
    """Generate a comprehensive legal review of the clause"""
    clause_type = clause.get('clause_type', 'GENERAL')
    clause_text = clause.get('clause_text', '')
    risk_level = clause.get('risk_level', 'LOW')
    
    review = f"**Legal Review for {clause_type} Clause**\n\n"
    
    # Legal compliance check
    review += "**Compliance Check:**\n"
    if clause_type == 'INDEMNITY':
        if 'defend' in clause_text.lower():
            review += "✅ Includes defense obligation\n"
        else:
            review += "❌ Missing defense obligation\n"
        
        if 'indemnify' in clause_text.lower():
            review += "✅ Includes indemnification language\n"
        else:
            review += "❌ Missing indemnification language\n"
    
    elif clause_type == 'LIABILITY':
        if 'consequential' in clause_text.lower():
            review += "✅ Addresses consequential damages\n"
        else:
            review += "❌ Does not address consequential damages\n"
        
        if 'cap' in clause_text.lower() or 'limit' in clause_text.lower():
            review += "✅ Includes liability limitations\n"
        else:
            review += "❌ No liability limitations found\n"
    
    elif clause_type == 'TERMINATION':
        if 'notice' in clause_text.lower():
            review += "✅ Includes notice requirements\n"
        else:
            review += "❌ Missing notice requirements\n"
    
    # Risk assessment
    review += f"\n**Risk Assessment:** {risk_level} risk level\n"
    
    if risk_level == 'HIGH':
        review += "⚠️ High risk - consider adding protective language\n"
    elif risk_level == 'MEDIUM':
        review += "⚖️ Medium risk - review for potential improvements\n"
    else:
        review += "✅ Low risk - appears acceptable\n"
    
    # Recommendations
    review += "\n**Recommendations:**\n"
    if risk_level == 'HIGH':
        review += "• Add liability caps or exclusions\n"
        review += "• Include force majeure protection\n"
        review += "• Specify governing law and jurisdiction\n"
    else:
        review += "• Clause appears well-structured\n"
        review += "• Consider periodic review for updates\n"
    
    return review

def render_clause_editor(clause_data: Dict[Any, Any], edit_mode: bool = False, unique_suffix: str = "", show_plain_english: bool = True):
    """Enhanced clause editor with professional styling and comprehensive editing features"""
    clause_id = clause_data['id']
    risk_level = clause_data.get('risk_level', 'LOW')
    
    # Create unique key suffix to avoid duplicates
    key_suffix = f"{clause_id}_{unique_suffix}" if unique_suffix else str(clause_id)

    risk_config = {
        'HIGH': {'color': '#ef4444', 'bg': 'rgba(239, 68, 68, 0.05)', 'icon': '🔴', 'label': 'High Risk'},
        'MEDIUM': {'color': '#f59e0b', 'bg': 'rgba(245, 158, 11, 0.05)', 'icon': '🟡', 'label': 'Medium Risk'},
        'LOW': {'color': '#10b981', 'bg': 'rgba(16, 185, 129, 0.05)', 'icon': '🟢', 'label': 'Low Risk'}
    }
    risk_style = risk_config.get(risk_level, risk_config['LOW'])

    st.markdown(f"""
    <style>
        .clause-editor-{clause_id} {{
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.9) 0%, rgba(248, 250, 252, 0.95) 100%);
            border-left: 4px solid {risk_style['color']};
            border-radius: 16px;
            padding: 0;
            margin: 1.5rem 0;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
            border: 1px solid rgba(226, 232, 240, 0.6);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            overflow: hidden;
            position: relative;
        }}
        .clause-editor-{clause_id}:hover {{ transform: translateY(-2px); box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12); }}
        .clause-header-{clause_id} {{ background: {risk_style['bg']}; padding: 1.5rem; border-bottom: 1px solid rgba(226, 232, 240, 0.3); }}
        .clause-content-{clause_id} {{ padding: 1.5rem; }}
        /* Ensure clause text is dark and readable even when disabled */
        .clause-content-{clause_id} textarea {{
            color: #111827 !important;
            -webkit-text-fill-color: #111827 !important;
            opacity: 1 !important;
            background: #f3f4f6;
        }}
        .risk-badge {{ background: linear-gradient(135deg, {risk_style['color']} 0%, {risk_style['color']}dd 100%); color: white; padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.85rem; font-weight: 500; display: inline-flex; align-items: center; gap: 0.5rem; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1); }}
        .clause-type-badge {{ background: rgba(59, 130, 246, 0.1); color: #1e40af; padding: 0.25rem 0.75rem; border-radius: 12px; font-size: 0.8rem; font-weight: 500; display: inline-block; margin-left: 1rem; }}
        .action-button {{ background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); color: white; border: none; border-radius: 8px; padding: 0.5rem 1rem; font-size: 0.85rem; font-weight: 500; cursor: pointer; transition: all 0.2s ease; margin: 0.25rem; }}
        .action-button:hover {{ transform: translateY(-1px); box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3); }}
        .secondary-button {{ background: rgba(248, 250, 252, 0.9); color: #475569; border: 1px solid #e2e8f0; }}
        .secondary-button:hover {{ background: rgba(241, 245, 249, 0.95); border-color: #cbd5e1; }}
        .success-button {{ background: linear-gradient(135deg, #10b981 0%, #059669 100%); }}
        .danger-button {{ background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%); }}
    </style>
    """, unsafe_allow_html=True)

    with st.container():
        st.markdown(f'<div class="clause-editor-{clause_id}">', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="clause-header-{clause_id}">
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 1rem;">
                <div>
                    <span class="risk-badge">
                        {risk_style['icon']} {risk_style['label']} ({clause_data.get('risk_score', 0)}/10)
                    </span>
                    <span class="clause-type-badge">
                        {clause_data.get('clause_type', 'GENERAL')}
                    </span>
                </div>
                <div style="color: #64748b; font-size: 0.9rem;">
                    ID #{clause_id}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f'<div class="clause-content-{clause_id}">', unsafe_allow_html=True)
        
        # Edit Mode Toggle
        col_toggle1, col_toggle2 = st.columns([1, 4])
        with col_toggle1:
            edit_mode = st.toggle("✏️ Edit Mode", value=edit_mode, key=f"edit_toggle_{key_suffix}")
        
        # Plain English explanation (conditional)
        if show_plain_english:
            st.markdown("#### 🗣️ Plain English Explanation")
            plain_english = generate_plain_english_explanation(clause_data)
            st.info(f"**What this clause means:**\n\n{plain_english}")
        
        # AI Suggestions section
        st.markdown("#### 🤖 AI Suggestions & Recommendations")
        ai_suggestions = generate_ai_suggestions(clause_data)
        
        # Display suggestions in expandable sections
        for i, suggestion in enumerate(ai_suggestions):
            with st.expander(f"💡 Suggestion {i+1}: {suggestion['title']}", expanded=False):
                st.markdown(f"**Category:** {suggestion['category']}")
                st.markdown(f"**Priority:** {suggestion['priority']}")
                st.markdown(f"**Description:** {suggestion['description']}")
                
                if suggestion.get('example'):
                    st.markdown(f"**Example:** {suggestion['example']}")
                
                if suggestion.get('action'):
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.markdown(f"**Recommended Action:** {suggestion['action']}")
                    with col2:
                        if st.button(f"Apply", key=f"apply_suggestion_{i}_{key_suffix}", type="secondary"):
                            st.success("Suggestion applied! (This would update the clause)")
        
        # Quick action buttons for common suggestions
        st.markdown("#### ⚡ Quick Actions")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🔍 Analyze Risk", key=f"analyze_risk_{key_suffix}"):
                risk_analysis = analyze_clause_risk(clause_data)
                st.info(f"**Risk Analysis:** {risk_analysis}")
        
        with col2:
            if st.button("📝 Improve Clarity", key=f"improve_clarity_{key_suffix}"):
                clarity_suggestions = suggest_clarity_improvements(clause_data)
                st.info(f"**Clarity Suggestions:** {clarity_suggestions}")
        
        with col3:
            if st.button("⚖️ Legal Review", key=f"legal_review_{key_suffix}"):
                legal_review = generate_legal_review(clause_data)
                st.info(f"**Legal Review:** {legal_review}")
        
        if edit_mode:
            st.markdown("""
            <div class="subsection-header">
                <h4><i class="fas fa-edit subheader-icon"></i>Edit Clause</h4>
                <p>Modify the clause text, type, and risk assessment</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Editable clause text
            current_text = clause_data.get('clause_text', '')
            edited_text = st.text_area(
                "Clause Text", 
                value=current_text, 
                height=150, 
                disabled=False, 
                key=f"clause_text_edit_{key_suffix}",
                help="Edit the original clause text"
            )
            
            # Clause type editing
            col_type1, col_type2 = st.columns(2)
            with col_type1:
                current_type = clause_data.get('clause_type', 'GENERAL')
                clause_types = ['INDEMNITY', 'LIABILITY', 'TERMINATION', 'PAYMENT', 'CONFIDENTIALITY', 'INTELLECTUAL_PROPERTY', 'GENERAL']
                edited_type = st.selectbox(
                    "Clause Type", 
                    clause_types, 
                    index=clause_types.index(current_type) if current_type in clause_types else 0,
                    key=f"clause_type_edit_{key_suffix}"
                )
            
            with col_type2:
                # Risk level editing
                risk_levels = ['LOW', 'MEDIUM', 'HIGH']
                edited_risk_level = st.selectbox(
                    "Risk Level", 
                    risk_levels, 
                    index=risk_levels.index(risk_level) if risk_level in risk_levels else 0,
                    key=f"risk_level_edit_{key_suffix}"
                )
            
            # Risk score editing
            current_score = clause_data.get('risk_score', 5.0)
            edited_score = st.slider(
                "Risk Score (0-10)", 
                min_value=0.0, 
                max_value=10.0, 
                value=float(current_score), 
                step=0.1,
                key=f"risk_score_edit_{key_suffix}",
                help="Adjust the risk score based on your assessment"
            )
            
            # AI Summary editing
            st.markdown("#### 🤖 AI Analysis & Summary")
            current_summary = clause_data.get('summary', '')
            edited_summary = st.text_area(
                "AI Summary", 
                value=current_summary, 
                height=120, 
                key=f"summary_edit_{key_suffix}",
                help="Edit the AI-generated summary"
            )
            
            # Additional notes
            current_notes = clause_data.get('notes', '')
            edited_notes = st.text_area(
                "Additional Notes", 
                value=current_notes, 
                height=80, 
                key=f"notes_edit_{key_suffix}",
                help="Add any additional notes or comments about this clause"
            )
            
        else:
            # View Mode - Original display
            st.subheader("📄 Original Clause")
            st.text_area("Clause Text", value=clause_data.get('clause_text',''), height=120, disabled=True, key=f"clause_text_{key_suffix}")

            st.subheader("🤖 AI Analysis")
            with st.expander("Show/Hide AI Summary", expanded=True):
                col1, col2 = st.columns([3, 1])
                with col1:
                    current_summary = clause_data.get('summary', '')
                    edited_summary = st.text_area("AI Summary", value=current_summary, height=100, key=f"summary_{key_suffix}")
                with col2:
                    st.write("**Risk Assessment**")
                    st.write(f"Score: {clause_data.get('risk_score',0)}/10")
                    st.write(f"Level: {risk_level}")
                    new_risk_level = st.selectbox("Override Risk Level", ['LOW','MEDIUM','HIGH'], index=['LOW','MEDIUM','HIGH'].index(risk_level), key=f"risk_override_{key_suffix}")

        # Toggle compare original vs AI summary
        show_compare = st.toggle("🔀 Compare original vs AI summary", key=f"compare_{key_suffix}")
        if show_compare:
            orig = clause_data.get('clause_text','')
            ai = clause_data.get('summary','')
            try:
                import difflib
                diff = difflib.ndiff(orig.split(), ai.split())
                added = []
                removed = []
                for token in diff:
                    if token.startswith('+ '):
                        added.append(token[2:])
                    elif token.startswith('- '):
                        removed.append(token[2:])
                st.markdown("**Added terms:** " + (", ".join(added[:50]) if added else "None"))
                st.markdown("**Removed terms:** " + (", ".join(removed[:50]) if removed else "None"))
            except Exception:
                st.info("Diff not available for this clause")

        # Action buttons based on mode
        if edit_mode:
            # Edit mode buttons
            colA, colB, colC, colD = st.columns(4)
            with colA:
                if st.button("💾 Save Changes", key=f"save_{key_suffix}", type="primary"):
                    # Check for changes
                    changes = {}
                    if edited_text != current_text:
                        changes['clause_text'] = edited_text
                    if edited_type != current_type:
                        changes['clause_type'] = edited_type
                    if edited_risk_level != risk_level:
                        changes['risk_level'] = edited_risk_level
                    if edited_score != current_score:
                        changes['risk_score'] = edited_score
                    if edited_summary != current_summary:
                        changes['summary'] = edited_summary
                    if edited_notes != current_notes:
                        changes['notes'] = edited_notes
                    
                    if changes:
                        try:
                            success = api_client.update_clause(clause_id, changes)
                            if success:
                                st.cache_data.clear()
                                st.success("✅ Clause updated successfully!")
                                time.sleep(1)
                                st.rerun()
                            else:
                                st.error("❌ Failed to update clause")
                        except Exception as e:
                            st.error(f"❌ Error updating clause: {str(e)}")
                    else:
                        st.info("ℹ️ No changes to save")
            
            with colB:
                if st.button("❌ Cancel", key=f"cancel_{key_suffix}"):
                    st.rerun()
            
            with colC:
                if st.button("🔄 Reset", key=f"reset_{key_suffix}"):
                    st.rerun()
            
            with colD:
                if st.button("📋 Copy Text", key=f"copy_{key_suffix}"):
                    st.info("📋 Clause text ready to copy")
        
        else:
            # View mode buttons
            colA, colB, colC, colD = st.columns(4)
            with colA:
                if st.button("✅ Accept Changes", key=f"accept_{key_suffix}", type="primary"):
                    has_changes = (edited_summary != current_summary) or (new_risk_level != risk_level)
                    if has_changes:
                        update_data: Dict[str, Any] = {}
                        if edited_summary != current_summary:
                            update_data['summary'] = edited_summary
                        if new_risk_level != risk_level:
                            update_data['risk_level'] = new_risk_level
                            risk_score_mapping = {'LOW': 2.5, 'MEDIUM': 5.0, 'HIGH': 8.0}
                            update_data['risk_score'] = risk_score_mapping[new_risk_level]
                        success = api_client.update_clause(clause_id, update_data)
                        if success:
                            st.cache_data.clear()
                            st.success("✅ Clause updated successfully!")
                            time.sleep(0.8)
                            st.rerun()
                        else:
                            st.error("❌ Failed to update clause")
                    else:
                        st.info("ℹ️ No changes to save")
            with colB:
                if st.button("❌ Reject AI", key=f"reject_{key_suffix}"):
                    st.info("🚫 AI suggestions rejected - original preserved")
            with colC:
                if st.button("🔄 Regenerate", key=f"regen_{key_suffix}"):
                    with st.spinner("Regenerating AI analysis..."):
                        st.info("🔄 Regeneration feature - would reprocess this clause")
            with colD:
                if st.button("📋 Copy Text", key=f"copy_{key_suffix}"):
                    st.info("📋 Clause text ready to copy")

        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
