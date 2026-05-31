import re

with open("frontend/app.py", "r", encoding="utf-8") as f:
    content = f.read()

def replace_empty_state(content, page_func, old_info, title, subtitle):
    # Find the function
    start = content.find(f"def {page_func}():")
    if start == -1: return content
    
    # Find the old info block
    old_block_start = content.find(old_info, start)
    if old_block_start == -1: return content
    
    # The block is usually: st.info("...")\n        return
    old_block_end = content.find("return", old_block_start) + 6
    
    new_empty_state = f"""        st.markdown('''
            <div style="text-align: center; padding: 4rem 2rem; background: white; border-radius: 12px; border: 1px dashed #cbd5e1; margin-top: 2rem;">
                <div style="font-size: 3rem; color: #94a3b8; margin-bottom: 1rem;">📄</div>
                <h3 style="color: #0f172a; margin-bottom: 0.5rem; font-size: 1.5rem;">{title}</h3>
                <p style="color: #64748b; margin-bottom: 1.5rem;">{subtitle}</p>
            </div>
        ''', unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("🚀 Upload First Document", type="primary", use_container_width=True, key=f"empty_upload_{page_func}"):
                st.session_state.current_page = "Upload"
                st.rerun()
        return"""
    
    return content[:old_block_start - 8] + new_empty_state + content[old_block_end:]

content = replace_empty_state(content, "render_dashboard_page", 'st.info("📊 No data available. Upload documents to see analytics.")', "No Documents Analyzed Yet", "Upload your first legal document to unlock the Interactive Analytics Dashboard.")
content = replace_empty_state(content, "render_clause_review_page", 'st.info("📝 No documents available for review. Upload documents first.")', "Clause Library Empty", "Upload a contract or agreement to extract and review clauses.")
content = replace_empty_state(content, "render_search_page", 'st.info("🔍 No documents available to search. Upload documents first.")', "Search Engine Inactive", "Your legal knowledge base is currently empty. Upload documents to start searching.")

with open("frontend/app.py", "w", encoding="utf-8") as f:
    f.write(content)
print("Updated empty states.")
