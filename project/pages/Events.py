import streamlit as st
import datetime
import utils.auth as auth
from components.sidebar import render_sidebar
from components.navbar import render_navbar
from utils.helpers import load_css, format_date
from utils.database import load_data, save_data, EVENTS_FILE, STUDENTS_FILE

# Set page config
st.set_page_config(page_title="Events Portal - Smart Campus", page_icon="🏆", layout="wide")

# Load CSS
load_css()

# Track page path
st.session_state.current_page = "Events"

# Enforce auth
user = auth.check_auth()

render_sidebar()
render_navbar("Campus Events Portal")

# Load database events
events = load_data(EVENTS_FILE)
students = load_data(STUDENTS_FILE)

# Sort events chronologically (earliest upcoming event first)
events = sorted(events, key=lambda x: x.get("date", ""))

st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.subheader("Upcoming Campus Events")
st.write("Browse campus events, check venues, and register to secure your seat.")
st.markdown('</div>', unsafe_allow_html=True)

if not events:
    st.info("There are no events listed at the moment. Check back later!")
else:
    # Render chronological list
    for idx, ev in enumerate(events):
        event_id = ev.get("id", idx)
        attendee_list = ev.get("attendees", [])
        is_registered = user.get("student_id", "") in attendee_list
        
        # Display event description and information
        st.markdown(
            f"""
            <div class="glass-card">
                <div style="display: flex; justify-content: space-between; align-items: baseline; flex-wrap: wrap;">
                    <h3 style="margin: 0; color: #4a90e2;">{ev.get('event', 'Unnamed Event')}</h3>
                    <span style="font-size: 0.9em; opacity: 0.8; font-weight: bold; background: rgba(74, 144, 226, 0.1); padding: 4px 10px; border-radius: 8px;">
                        📅 {format_date(ev.get('date', ''))}
                    </span>
                </div>
                <div style="margin-top: 10px; font-size: 0.95em; opacity: 0.85;">
                    📍 <strong>Venue:</strong> {ev.get('venue', 'To Be Decided')}
                </div>
                <p style="margin-top: 15px; font-size: 1.05em; line-height: 1.6;">{ev.get('description', '')}</p>
                <div style="margin-top: 10px; font-size: 0.9em; color: #a5b4fc;">
                    👥 Total Registered Attendees: <strong>{len(attendee_list)}</strong>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Actions
        if user["role"] == "student":
            stu_id = user.get("student_id", "")
            btn_key = f"evt_reg_{event_id}"
            
            if is_registered:
                if st.button("🔴 Cancel My Registration", key=btn_key):
                    # Unregister user
                    attendee_list.remove(stu_id)
                    ev["attendees"] = attendee_list
                    save_data(EVENTS_FILE, events)
                    st.success("You have unregistered from this event.")
                    st.rerun()
            else:
                if st.button("🟢 Register for Event", key=btn_key):
                    # Register user
                    attendee_list.append(stu_id)
                    ev["attendees"] = attendee_list
                    save_data(EVENTS_FILE, events)
                    st.success("🎉 You are registered for this event!")
                    st.rerun()
        else:
            # Faculty/Admin detailed attendee view
            if attendee_list:
                with st.expander(f"View Attendees list ({len(attendee_list)} students registered)"):
                    # Map attendee IDs to student details
                    stu_details = []
                    for sid in attendee_list:
                        s_record = next((s for s in students if s["student_id"] == sid), None)
                        if s_record:
                            stu_details.append({
                                "Student ID": s_record["student_id"],
                                "Name": s_record["name"],
                                "Department": s_record["department"],
                                "Email": s_record["email"]
                            })
                    if stu_details:
                        st.table(stu_details)
                    else:
                        st.info("Registered student records not found.")
            else:
                st.info("No students registered for this event yet.")
        
        st.markdown("<br>", unsafe_allow_html=True)
