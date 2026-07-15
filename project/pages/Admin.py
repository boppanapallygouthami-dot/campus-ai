import streamlit as st
import datetime
import utils.auth as auth
import utils.validators as val
from components.sidebar import render_sidebar
from components.navbar import render_navbar
from utils.helpers import load_css
from utils.database import (
    load_data, save_data, 
    USERS_FILE, STUDENTS_FILE, NOTICES_FILE, EVENTS_FILE, COMPLAINTS_FILE
)

# Set page config
st.set_page_config(page_title="Admin Panel - Smart Campus", page_icon="🛡️", layout="wide")

# Load CSS
load_css()

# Track page path
st.session_state.current_page = "Admin Panel"

# Enforce auth (ONLY ADMINS ALLOWED)
user = auth.check_auth(required_roles=["admin"])

render_sidebar()
render_navbar("Administrator Portal")

# Load databases
users = load_data(USERS_FILE)
students = load_data(STUDENTS_FILE)
notices = load_data(NOTICES_FILE)
events = load_data(EVENTS_FILE)
complaints = load_data(COMPLAINTS_FILE)

# Tabs structure
tab_students, tab_notices, tab_events, tab_complaints = st.tabs([
    "👥 Manage Students", 
    "📢 Notice Coordinator", 
    "🏆 Event Board Controller", 
    "⚠️ System Logs & Reports"
])

# ----------------- TAB 1: STUDENT MANAGEMENT -----------------
with tab_students:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("Add New Student Profile")
    
    with st.form("admin_add_student_form", clear_on_submit=True):
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            stu_name = st.text_input("Full Name")
            stu_id_raw = st.text_input("Student ID (e.g. STU102)")
            stu_dept = st.selectbox("Department", options=["Computer Science", "Electrical Engineering", "Mechanical Engineering", "Civil Engineering", "Business Administration", "Physics"])
            stu_year = st.selectbox("Current Year", options=["1st Year", "2nd Year", "3rd Year", "4th Year"])
        with col_s2:
            stu_email = st.text_input("Campus Email Address")
            stu_mobile = st.text_input("Mobile Number (10 digits)")
            stu_password = st.text_input("Initial Password", type="password")
            
        stu_submit = st.form_submit_button("Add Student")
        
        if stu_submit:
            # Validations
            if not stu_name or not stu_id_raw or not stu_email or not stu_mobile or not stu_password:
                st.error("Please fill in all fields.")
            elif not val.validate_student_id(stu_id_raw):
                st.error("Student ID must be alphanumeric and 3-15 characters.")
            elif not val.validate_email(stu_email):
                st.error("Invalid email address.")
            elif not val.validate_mobile(stu_mobile):
                st.error("Mobile number must be exactly 10 digits.")
            elif not val.validate_password(stu_password):
                st.error("Password must satisfy standard safety requirements.")
            else:
                # Check duplicate email/ID
                dup_email = any(u["email"].lower() == stu_email.lower() for u in users)
                dup_id = any(u.get("student_id", "").upper() == stu_id_raw.upper() for u in users)
                
                if dup_email or dup_id:
                    st.error("Student ID or email already registered.")
                else:
                    # Save to users.json
                    new_user_id = max([u["id"] for u in users], default=0) + 1
                    users.append({
                        "id": new_user_id,
                        "name": stu_name,
                        "student_id": stu_id_raw.upper(),
                        "department": stu_dept,
                        "email": stu_email,
                        "mobile": stu_mobile,
                        "password": auth.hash_password(stu_password),
                        "role": "student"
                    })
                    save_data(USERS_FILE, users)
                    
                    # Save to students.json
                    new_stu_id = max([s["id"] for s in students], default=0) + 1
                    students.append({
                        "id": new_stu_id,
                        "student_id": stu_id_raw.upper(),
                        "name": stu_name,
                        "department": stu_dept,
                        "email": stu_email,
                        "mobile": stu_mobile,
                        "year": stu_year,
                        "attendance": 100.0
                    })
                    save_data(STUDENTS_FILE, students)
                    st.success(f"🎉 Successfully created profile for student {stu_name}!")
                    st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # Edit & Delete Students
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("Edit / Delete Student Profiles")
    
    student_list = {s["student_id"]: f"{s['name']} ({s['student_id']})" for s in students}
    
    if not student_list:
        st.info("No registered students found.")
    else:
        selected_stu = st.selectbox("Select Student to Edit/Delete", options=list(student_list.keys()), format_func=lambda x: student_list[x])
        
        # Load active info
        stu_record = next((s for s in students if s["student_id"] == selected_stu), None)
        user_record = next((u for u in users if u.get("student_id") == selected_stu), None)
        
        if stu_record:
            col_ed1, col_ed2 = st.columns(2)
            with col_ed1:
                edit_name = st.text_input("Name", value=stu_record.get("name", ""), key="ed_name")
                edit_dept = st.selectbox("Dept", options=["Computer Science", "Electrical Engineering", "Mechanical Engineering", "Civil Engineering", "Business Administration", "Physics"], index=0, key="ed_dept")
            with col_ed2:
                edit_mobile = st.text_input("Mobile", value=stu_record.get("mobile", ""), key="ed_mobile")
                edit_year = st.selectbox("Year", options=["1st Year", "2nd Year", "3rd Year", "4th Year"], key="ed_year")
            
            sub_col1, sub_col2, _ = st.columns([1, 1, 2])
            with sub_col1:
                if st.button("💾 Save Profile Changes"):
                    if not edit_name or not edit_mobile:
                        st.error("Fields cannot be empty.")
                    elif not val.validate_mobile(edit_mobile):
                        st.error("Mobile must be 10 digits.")
                    else:
                        stu_record["name"] = edit_name
                        stu_record["department"] = edit_dept
                        stu_record["mobile"] = edit_mobile
                        stu_record["year"] = edit_year
                        save_data(STUDENTS_FILE, students)
                        
                        if user_record:
                            user_record["name"] = edit_name
                            user_record["department"] = edit_dept
                            user_record["mobile"] = edit_mobile
                            save_data(USERS_FILE, users)
                            
                        st.success("Changes saved successfully!")
                        st.rerun()
            with sub_col2:
                if st.button("🗑️ Delete Student Account"):
                    # Remove from students.json
                    students.remove(stu_record)
                    save_data(STUDENTS_FILE, students)
                    
                    # Remove from users.json
                    if user_record:
                        users.remove(user_record)
                        save_data(USERS_FILE, users)
                        
                    st.success("Student profile and account deleted.")
                    st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)


# ----------------- TAB 2: NOTICE BOARD CONTROL -----------------
with tab_notices:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("📢 Post New Announcement Notice")
    
    with st.form("admin_notice_form", clear_on_submit=True):
        not_title = st.text_input("Notice Title", placeholder="e.g. End Semester Exam Fee Payment Deadline")
        not_desc = st.text_area("Announcement Description Details")
        not_cat = st.selectbox("Notice Category", options=["Academics", "Events", "Examinations", "Placements", "General"])
        
        not_submit = st.form_submit_button("Publish Notice")
        
        if not_submit:
            if not not_title or not not_desc:
                st.error("Notice Title and Description are required.")
            else:
                new_not_id = max([n["id"] for n in notices], default=0) + 1
                notices.append({
                    "id": new_not_id,
                    "title": not_title,
                    "description": not_desc,
                    "category": not_cat,
                    "date": datetime.date.today().isoformat()
                })
                save_data(NOTICES_FILE, notices)
                st.success("🎉 Announcement posted to the campus Notice board successfully!")
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # Delete notices
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("Manage / Delete Active Notices")
    
    if not notices:
        st.info("No notices published.")
    else:
        for idx, n in enumerate(notices):
            st.markdown(f"**{n.get('title')}** (Published: {n.get('date')} | Category: {n.get('category')})")
            if st.button("🗑️ Delete Notice", key=f"del_not_{n.get('id', idx)}"):
                notices.remove(n)
                save_data(NOTICES_FILE, notices)
                st.success("Notice deleted.")
                st.rerun()
            st.markdown("<hr style='opacity: 0.1;'>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ----------------- TAB 3: EVENT COORDINATOR -----------------
with tab_events:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("🏆 Schedule New Campus Event")
    
    with st.form("admin_event_form", clear_on_submit=True):
        evt_title = st.text_input("Event Name")
        evt_venue = st.text_input("Venue Location", placeholder="e.g. Auditorium, Seminar Room B")
        evt_date = st.date_input("Event Scheduled Date", value=datetime.date.today() + datetime.timedelta(days=7))
        evt_desc = st.text_area("Event Details & Requirements")
        
        evt_submit = st.form_submit_button("Publish Event")
        
        if evt_submit:
            if not evt_title or not evt_venue or not evt_desc:
                st.error("All event fields are required.")
            else:
                new_evt_id = max([e["id"] for e in events], default=0) + 1
                events.append({
                    "id": new_evt_id,
                    "event": evt_title,
                    "venue": evt_venue,
                    "date": evt_date.isoformat(),
                    "description": evt_desc,
                    "attendees": []
                })
                save_data(EVENTS_FILE, events)
                st.success(f"🎉 Event '{evt_title}' scheduled successfully!")
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # Delete events
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("Manage / Delete Active Events")
    
    if not events:
        st.info("No events scheduled.")
    else:
        for idx, ev in enumerate(events):
            st.markdown(f"**{ev.get('event')}** (Date: {ev.get('date')} | Venue: {ev.get('venue')})")
            if st.button("🗑️ Delete Event", key=f"del_evt_{ev.get('id', idx)}"):
                events.remove(ev)
                save_data(EVENTS_FILE, events)
                st.success("Event deleted.")
                st.rerun()
            st.markdown("<hr style='opacity: 0.1;'>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ----------------- TAB 4: SYSTEM LOGS & COMPLAINTS -----------------
with tab_complaints:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("📊 Complaint Logs Status Overview")
    
    total_c = len(complaints)
    pending_c = len([c for c in complaints if c.get("status") == "Pending"])
    progress_c = len([c for c in complaints if c.get("status") == "In Progress"])
    resolved_c = len([c for c in complaints if c.get("status") == "Resolved"])
    
    col_c1, col_c2, col_c3, col_c4 = st.columns(4)
    with col_c1:
        st.metric("Total Complaints Filed", total_c)
    with col_c2:
        st.metric("Pending Action", pending_c)
    with col_c3:
        st.metric("In Progress Investigation", progress_c)
    with col_c4:
        st.metric("Successfully Resolved", resolved_c)
        
    st.markdown("<br>", unsafe_allow_html=True)
    st.write("💡 Details of individual complaints, along with progress tracking actions, can be found in the [Complaints Portal](file:///pages/Complaints.py).")
    st.markdown('</div>', unsafe_allow_html=True)
