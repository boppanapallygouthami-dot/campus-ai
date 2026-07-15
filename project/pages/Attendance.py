import streamlit as st
import pandas as pd
import datetime
import utils.auth as auth
from components.sidebar import render_sidebar
from components.navbar import render_navbar
from utils.helpers import load_css, export_to_csv
from utils.database import load_data, save_data, ATTENDANCE_FILE, STUDENTS_FILE

# Page configuration
st.set_page_config(page_title="Attendance - Smart Campus", page_icon="📅", layout="wide")

# Load styles
load_css()

# Track page path
st.session_state.current_page = "Attendance"

# Enforce auth
user = auth.check_auth()

render_sidebar()
render_navbar("Attendance Management")

# Load records
attendance_records = load_data(ATTENDANCE_FILE)
students = load_data(STUDENTS_FILE)

# Helper function to compute attendance percentage
def get_attendance_percent(stu_id: str, records: list) -> float:
    stu_records = [r for r in records if r["student_id"] == stu_id]
    if not stu_records:
        return 100.0
    presents = len([r for r in stu_records if r["status"] == "Present"])
    return round((presents / len(stu_records)) * 100, 1)

if user["role"] == "student":
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("Your Attendance Summary")
    
    # Calculate current student stats
    stu_id = user.get("student_id", "")
    my_records = [r for r in attendance_records if r["student_id"] == stu_id]
    
    pct = get_attendance_percent(stu_id, attendance_records)
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown(
            f"""
            <div style="text-align: center; padding: 20px; background: rgba(255,255,255,0.05); border-radius: 12px; border: 1px solid rgba(255,255,255,0.1);">
                <span style="font-size: 1.1em; opacity: 0.7;">Your Attendance Rate</span>
                <h1 style="color: #4a90e2; font-size: 3em; margin: 10px 0;">{pct}%</h1>
                <p style="margin: 0; font-size: 0.9em; opacity: 0.6;">Total Classes Recorded: {len(my_records)}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    with col2:
        # Check-in feature
        st.markdown("### 🕒 Daily Self Check-in")
        today_str = datetime.date.today().isoformat()
        
        # Check if already marked for today
        already_marked = any(r["student_id"] == stu_id and r["date"] == today_str for r in attendance_records)
        
        if already_marked:
            st.success("✅ You have already checked in for today.")
        else:
            st.info("You haven't checked in for today yet. Mark your presence below.")
            if st.button("Mark Present Today"):
                new_record = {
                    "student_id": stu_id,
                    "date": today_str,
                    "status": "Present"
                }
                attendance_records.append(new_record)
                save_data(ATTENDANCE_FILE, attendance_records)
                
                # Update student overall attendance cached value in students.json
                for s in students:
                    if s["student_id"] == stu_id:
                        s["attendance"] = get_attendance_percent(stu_id, attendance_records)
                save_data(STUDENTS_FILE, students)
                
                st.success("🎉 Checked in successfully!")
                st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)
    
    # 2. Filter and View Table
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("Attendance History Logs")
    
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        start_date = st.date_input("Start Date", value=datetime.date.today() - datetime.timedelta(days=30))
    with col_f2:
        end_date = st.date_input("End Date", value=datetime.date.today())
        
    filtered_records = []
    for r in my_records:
        try:
            r_date = datetime.date.fromisoformat(r["date"])
            if start_date <= r_date <= end_date:
                filtered_records.append(r)
        except ValueError:
            pass

    if filtered_records:
        df_filtered = pd.DataFrame(filtered_records)
        st.dataframe(df_filtered[["date", "status"]], use_container_width=True)
        
        # CSV Export
        csv_bytes = export_to_csv(filtered_records)
        st.download_button(
            label="📥 Export Logs to CSV",
            data=csv_bytes,
            file_name=f"attendance_{stu_id}_{today_str}.csv",
            mime="text/csv"
        )
    else:
        st.warning("No logs found for the selected date range.")
    st.markdown('</div>', unsafe_allow_html=True)

# Admin view
else:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("Faculty & Admin Attendance Panel")
    
    # Selection of Student
    student_options = {s["student_id"]: f"{s['name']} ({s['student_id']}) - {s['department']}" for s in students}
    
    if not student_options:
        st.warning("No student profiles registered in system yet.")
    else:
        selected_id = st.selectbox("Select Student Profile", options=list(student_options.keys()), format_func=lambda x: student_options[x])
        
        stu_records = [r for r in attendance_records if r["student_id"] == selected_id]
        stu_pct = get_attendance_percent(selected_id, attendance_records)
        
        st.markdown(
            f"""
            <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.05); padding: 15px; border-radius: 8px; margin-bottom: 20px;">
                <span style="font-size: 1.1em; font-weight: 600;">Overall Attendance Percentage: </span>
                <span style="color:#4a90e2; font-size: 1.5em; font-weight: 700;">{stu_pct}%</span>
                <p style="margin: 5px 0 0 0; font-size: 0.85em; opacity: 0.7;">Total recorded lectures: {len(stu_records)}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Manual Attendance Action for selected student
        st.markdown("### ✍️ Log New Attendance Record")
        col_m1, col_m2, col_m3 = st.columns(3)
        with col_m1:
            log_date = st.date_input("Date of Record", value=datetime.date.today(), key="admin_log_date")
        with col_m2:
            log_status = st.selectbox("Status", options=["Present", "Absent"])
        with col_m3:
            st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
            log_submit = st.button("Save Record")
            
        if log_submit:
            date_str = log_date.isoformat()
            
            # Check if duplicate date
            existing_idx = next((i for i, r in enumerate(attendance_records) if r["student_id"] == selected_id and r["date"] == date_str), None)
            
            if existing_idx is not None:
                attendance_records[existing_idx]["status"] = log_status
                st.info(f"Updated existing attendance record for {date_str} to: {log_status}")
            else:
                attendance_records.append({
                    "student_id": selected_id,
                    "date": date_str,
                    "status": log_status
                })
                st.success(f"Added attendance record for {date_str} as: {log_status}")
                
            save_data(ATTENDANCE_FILE, attendance_records)
            
            # Update student overall cached percentage
            for s in students:
                if s["student_id"] == selected_id:
                    s["attendance"] = get_attendance_percent(selected_id, attendance_records)
            save_data(STUDENTS_FILE, students)
            
            st.rerun()

        # View and Export Student Logs
        st.markdown("---")
        st.subheader("Record History")
        
        if stu_records:
            df_stu = pd.DataFrame(stu_records)
            st.dataframe(df_stu[["date", "status"]], use_container_width=True)
            
            # CSV Download
            csv_bytes = export_to_csv(stu_records)
            st.download_button(
                label="📥 Export Student Attendance CSV",
                data=csv_bytes,
                file_name=f"attendance_report_{selected_id}.csv",
                mime="text/csv"
            )
        else:
            st.info("No recorded logs found for this student.")
            
    st.markdown('</div>', unsafe_allow_html=True)
