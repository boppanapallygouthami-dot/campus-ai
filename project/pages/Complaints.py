import streamlit as st
import datetime
import utils.auth as auth
from components.sidebar import render_sidebar
from components.navbar import render_navbar
from utils.helpers import load_css, format_date
from utils.database import load_data, save_data, COMPLAINTS_FILE

# Set page config
st.set_page_config(page_title="Complaints Portal - Smart Campus", page_icon="⚠️", layout="wide")

# Load CSS
load_css()

# Track page path
st.session_state.current_page = "Complaints"

# Enforce auth
user = auth.check_auth()

render_sidebar()
render_navbar("Complaint Resolution Portal")

# Load DB data
complaints = load_data(COMPLAINTS_FILE)

# Sort complaints (newest first)
complaints = sorted(complaints, key=lambda x: x.get("date", ""), reverse=True)

# Helper function to get status colors
def get_status_style(status: str) -> str:
    if status == "Pending":
        return "background-color: #ef4444; color: white;"
    elif status == "In Progress":
        return "background-color: #f59e0b; color: white;"
    else:  # Resolved
        return "background-color: #10b981; color: white;"

# If user is a student: Submit and View own complaints
if user["role"] == "student":
    stu_id = user.get("student_id", "")
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("📢 Submit a New Complaint")
    
    with st.form("new_complaint_form", clear_on_submit=True):
        issue_title = st.text_input("Complaint Topic / Subject", placeholder="e.g. WiFi issue in Hostel, Lab computer breakdown")
        issue_desc = st.text_area("Detailed Description of the Problem", placeholder="Please provide specific details...")
        
        submitted = st.form_submit_button("Submit Complaint")
        
        if submitted:
            if not issue_title or not issue_desc:
                st.error("Please fill in both the Subject and Description fields.")
            else:
                new_id = max([c["id"] for c in complaints], default=0) + 1
                new_complaint = {
                    "id": new_id,
                    "student_id": stu_id,
                    "student": user["name"],
                    "issue": f"{issue_title}: {issue_desc}",
                    "status": "Pending",
                    "date": datetime.date.today().isoformat()
                }
                complaints.append(new_complaint)
                save_data(COMPLAINTS_FILE, complaints)
                st.success("🎉 Complaint submitted successfully. Our maintenance team will review it shortly.")
                st.rerun()
                
    st.markdown('</div>', unsafe_allow_html=True)

    # Display Student's Complaint History
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("📜 Your Complaint History & Status Tracking")
    
    my_complaints = [c for c in complaints if c.get("student_id") == stu_id]
    
    if not my_complaints:
        st.info("You haven't filed any complaints yet.")
    else:
        for comp in my_complaints:
            st.markdown(
                f"""
                <div style="
                    border-left: 5px solid { '#ef4444' if comp['status'] == 'Pending' else '#f59e0b' if comp['status'] == 'In Progress' else '#10b981' }; 
                    background: rgba(255,255,255,0.03); 
                    padding: 15px; 
                    border-radius: 8px; 
                    margin-bottom: 15px;
                ">
                    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
                        <span style="font-size: 0.85em; font-weight: bold; {get_status_style(comp.get('status', 'Pending'))} padding: 2px 8px; border-radius: 12px;">
                            {comp.get('status', 'Pending').upper()}
                        </span>
                        <span style="font-size: 0.85em; opacity: 0.7;">
                            📅 Filed: {format_date(comp.get('date', ''))}
                        </span>
                    </div>
                    <p style="margin: 10px 0 0 0; font-size: 1.05em; line-height: 1.5; color: white;">{comp.get('issue', '')}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
            
    st.markdown('</div>', unsafe_allow_html=True)

# Admin panel view for complaints management
else:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("🔧 Manage Campus Complaints")
    
    col_af1, col_af2 = st.columns([1, 2])
    with col_af1:
        status_filter = st.selectbox("Filter by Status", options=["All", "Pending", "In Progress", "Resolved"])
        
    filtered_complaints = []
    for c in complaints:
        if status_filter != "All" and c.get("status") != status_filter:
            continue
        filtered_complaints.append(c)

    if not filtered_complaints:
        st.info("No complaints found with current filters.")
    else:
        for idx, comp in enumerate(filtered_complaints):
            comp_id = comp.get("id", idx)
            st.markdown(
                f"""
                <div style="
                    border-left: 5px solid { '#ef4444' if comp['status'] == 'Pending' else '#f59e0b' if comp['status'] == 'In Progress' else '#10b981' }; 
                    background: rgba(255,255,255,0.03); 
                    padding: 15px; 
                    border-radius: 8px; 
                    margin-bottom: 15px;
                ">
                    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
                        <span style="font-size: 0.85em; font-weight: bold; {get_status_style(comp.get('status', 'Pending'))} padding: 2px 8px; border-radius: 12px;">
                            {comp.get('status', 'Pending').upper()}
                        </span>
                        <span style="font-size: 0.85em; opacity: 0.7;">
                            📅 Filed: {format_date(comp.get('date', ''))} | 👤 Student: <strong>{comp.get('student', 'Anonymous')} ({comp.get('student_id', '')})</strong>
                        </span>
                    </div>
                    <p style="margin: 10px 0; font-size: 1.05em; color: white;">{comp.get('issue', '')}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # Action: Status updates
            btn_col1, btn_col2, btn_col3 = st.columns([1, 1, 2])
            with btn_col1:
                if comp["status"] != "In Progress":
                    if st.button("🚧 Work on Issue", key=f"btn_w_{comp_id}"):
                        comp["status"] = "In Progress"
                        save_data(COMPLAINTS_FILE, complaints)
                        st.success(f"Complaint status updated.")
                        st.rerun()
            with btn_col2:
                if comp["status"] != "Resolved":
                    if st.button("✅ Mark Resolved", key=f"btn_r_{comp_id}"):
                        comp["status"] = "Resolved"
                        save_data(COMPLAINTS_FILE, complaints)
                        st.success(f"Complaint status updated.")
                        st.rerun()
            with btn_col3:
                # Spacer
                pass
            st.markdown("<hr style='opacity:0.1; margin:10px 0;'>", unsafe_allow_html=True)
            
    st.markdown('</div>', unsafe_allow_html=True)
