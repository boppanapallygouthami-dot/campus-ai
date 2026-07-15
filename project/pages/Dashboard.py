import streamlit as st
import utils.auth as auth
from components.sidebar import render_sidebar
from components.navbar import render_navbar
from components.cards import render_metric_cards
from components.charts import render_attendance_chart, render_department_chart, render_monthly_activities
from utils.helpers import load_css
from utils.database import load_data, STUDENTS_FILE, FACULTY_FILE, ATTENDANCE_FILE, NOTICES_FILE, EVENTS_FILE, COMPLAINTS_FILE

# Set page config
st.set_page_config(page_title="Dashboard - Smart Campus", page_icon="🏫", layout="wide")

# Load CSS
load_css()

# Track page path
st.session_state.current_page = "Dashboard"

# Enforce auth
user = auth.check_auth()

# Render Layout
render_sidebar()
render_navbar(f"Welcome, {user.get('name', 'User')}")

# Load DB data for metrics and charting
students = load_data(STUDENTS_FILE)
faculty = load_data(FACULTY_FILE)
attendance = load_data(ATTENDANCE_FILE)
notices = load_data(NOTICES_FILE)
events = load_data(EVENTS_FILE)
complaints = load_data(COMPLAINTS_FILE)

# Calculate statistics
total_students = len(students)
total_faculty = len(faculty)

if total_students > 0:
    avg_attendance = round(sum(s.get("attendance", 100) for s in students) / total_students, 1)
else:
    avg_attendance = 0.0

active_events = len(events)
total_notices = len(notices)

# Show only non-resolved complaints in the count
pending_complaints = len([c for c in complaints if c.get("status") in ["Pending", "In Progress"]])

stats = {
    "total_students": total_students,
    "total_faculty": total_faculty,
    "attendance_pct": avg_attendance,
    "active_events": active_events,
    "total_notices": total_notices,
    "total_complaints": pending_complaints
}

# 1. Render Top Metric Cards
render_metric_cards(stats)

st.markdown("<br>", unsafe_allow_html=True)

# 2. Render Charts
st.markdown("### 📊 Analytics & Reports")
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    render_attendance_chart(attendance)
    st.markdown('</div>', unsafe_allow_html=True)

with col_chart2:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    render_department_chart(students)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="glass-card">', unsafe_allow_html=True)
render_monthly_activities(events)
st.markdown('</div>', unsafe_allow_html=True)

# 3. Quick Actions
st.markdown("### ⚡ Quick Access Actions")
col_act1, col_act2, col_act3, col_act4 = st.columns(4)

with col_act1:
    if st.button("Mark/View Attendance"):
        st.session_state.current_page = "Attendance"
        st.switch_page("pages/Attendance.py")

with col_act2:
    if st.button("View Notice Board"):
        st.session_state.current_page = "Notices"
        st.switch_page("pages/Notices.py")

with col_act3:
    if st.button("Submit Complaint"):
        st.session_state.current_page = "Complaints"
        st.switch_page("pages/Complaints.py")

with col_act4:
    if st.button("Browse Campus Events"):
        st.session_state.current_page = "Events"
        st.switch_page("pages/Events.py")
