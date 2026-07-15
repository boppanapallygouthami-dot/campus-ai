import streamlit as st
import pandas as pd
import datetime
import utils.auth as auth
from components.sidebar import render_sidebar
from components.navbar import render_navbar
from utils.helpers import load_css, generate_pdf_text_content, format_date
from utils.database import load_data, NOTICES_FILE

# Set page config
st.set_page_config(page_title="Notice Board - Smart Campus", page_icon="📢", layout="wide")

# Load CSS
load_css()

# Track page path
st.session_state.current_page = "Notices"

# Enforce auth
user = auth.check_auth()

render_sidebar()
render_navbar("Campus Notice Board")

# Load database notices
notices = load_data(NOTICES_FILE)

# Sort notices so the latest is on top
notices = sorted(notices, key=lambda x: x.get("date", ""), reverse=True)

st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.subheader("Search and Filter Notices")

col1, col2 = st.columns([2, 1])
with col1:
    search_query = st.text_input("🔍 Search notices by title or content", placeholder="Enter keywords...")
with col2:
    categories = ["All", "Academics", "Events", "Examinations", "Placements", "General"]
    selected_category = st.selectbox("Category Filter", options=categories)

# Apply filters
filtered_notices = []
for n in notices:
    # Category match
    if selected_category != "All" and n.get("category", "") != selected_category:
        continue
    # Search match
    if search_query:
        query = search_query.lower()
        title_match = query in n.get("title", "").lower()
        desc_match = query in n.get("description", "").lower()
        if not (title_match or desc_match):
            continue
    filtered_notices.append(n)

st.markdown('</div>', unsafe_allow_html=True)

# Display Notices
if not filtered_notices:
    st.info("No notices found matching the filters.")
else:
    for idx, notice in enumerate(filtered_notices):
        # Category badge color selector
        cat_colors = {
            "Academics": "#3b82f6",
            "Events": "#8b5cf6",
            "Examinations": "#ef4444",
            "Placements": "#10b981",
            "General": "#6b7280"
        }
        badge_color = cat_colors.get(notice.get("category", ""), "#4a90e2")
        
        st.markdown(
            f"""
            <div class="glass-card" style="margin-bottom: 25px;">
                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
                    <span style="font-size: 0.85em; font-weight: bold; background-color: {badge_color}; color: white; padding: 3px 10px; border-radius: 12px; margin-bottom: 8px;">
                        {notice.get('category', 'General').upper()}
                    </span>
                    <span style="font-size: 0.85em; opacity: 0.7; margin-bottom: 8px;">
                        📅 Date Published: {format_date(notice.get('date', ''))}
                    </span>
                </div>
                <h3 style="margin-top: 10px; color: white;">{notice.get('title', 'Untitled Notice')}</h3>
                <p style="opacity: 0.9; line-height: 1.6; font-size: 1.05em;">{notice.get('description', '')}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Prepare notice download content
        text_content = generate_pdf_text_content(
            title=notice.get("title", "Notice"),
            content=notice.get("description", ""),
            date_str=notice.get("date", datetime.date.today().isoformat())
        )
        
        # Unique key for download button
        download_key = f"dl_notice_{notice.get('id', idx)}"
        st.download_button(
            label="📄 Download Official Announcement (TXT)",
            data=text_content,
            file_name=f"Notice_{notice.get('id', idx)}.txt",
            mime="text/plain",
            key=download_key
        )
        st.markdown("<br><br>", unsafe_allow_html=True)
