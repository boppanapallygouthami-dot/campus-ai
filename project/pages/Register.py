import streamlit as st
import utils.auth as auth
import utils.validators as val
from components.authentication import render_auth_header, render_auth_footer
from utils.helpers import load_css
from utils.database import USERS_FILE, STUDENTS_FILE, load_data, save_data
from pathlib import Path
import base64

# Page configurations
st.set_page_config(page_title="Register - Smart Campus", page_icon="📝", layout="centered")

# Load styles.css
load_css()

# Track page path
st.session_state.current_page = "Register"

# Render custom background
bg_path = Path(__file__).resolve().parent.parent / "assets" / "background.jpg"
if bg_path.exists():
    try:
        with open(bg_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: linear-gradient(rgba(15, 23, 42, 0.75), rgba(15, 23, 42, 0.85)), url("data:image/jpeg;base64,{encoded_string}");
                background-size: cover;
                background-position: center;
                background-attachment: fixed;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
    except Exception:
        pass

with st.container():
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    
    render_auth_header("Register", "Create your Smart Campus student account")

    # Inputs
    name = st.text_input("Full Name", placeholder="e.g. Alice Smith")
    student_id = st.text_input("Student ID / ID Number", placeholder="e.g. STU123")
    
    departments = ["Computer Science", "Electrical Engineering", "Mechanical Engineering", "Civil Engineering", "Business Administration", "Physics"]
    department = st.selectbox("Department", options=departments)
    
    email = st.text_input("Campus Email Address", placeholder="e.g. alice@campus.com")
    mobile = st.text_input("Mobile Number (10 digits)", placeholder="e.g. 9876543210")
    
    password = st.text_input("Password", type="password", placeholder="Choose a strong password")
    confirm_password = st.text_input("Confirm Password", type="password", placeholder="Repeat your password")

    st.markdown("<br>", unsafe_allow_html=True)
    register_submitted = st.button("Register Account")

    if register_submitted:
        # Form Validation
        if not name or not student_id or not email or not mobile or not password or not confirm_password:
            st.error("Please fill in all fields.")
        elif not val.validate_student_id(student_id):
            st.error("Student ID must be alphanumeric and between 3-15 characters.")
        elif not val.validate_email(email):
            st.error("Invalid email format.")
        elif not val.validate_mobile(mobile):
            st.error("Mobile number must be exactly 10 digits.")
        elif password != confirm_password:
            st.error("Passwords do not match.")
        elif not val.validate_password(password):
            st.error(
                "Password must be at least 8 characters long and contain "
                "at least one uppercase letter, one lowercase letter, one digit, and one special character."
            )
        else:
            # Check duplicate user
            users = load_data(USERS_FILE)
            duplicate_email = any(u["email"].lower() == email.lower() for u in users)
            duplicate_id = any(u.get("student_id", "").upper() == student_id.upper() for u in users)

            if duplicate_email:
                st.error("An account with this email address already exists.")
            elif duplicate_id:
                st.error("An account with this Student ID already exists.")
            else:
                # Add to users.json
                new_user_id = max([u["id"] for u in users], default=0) + 1
                new_user = {
                    "id": new_user_id,
                    "name": name,
                    "student_id": student_id.upper(),
                    "department": department,
                    "email": email,
                    "mobile": mobile,
                    "password": auth.hash_password(password),
                    "role": "student"
                }
                users.append(new_user)
                save_data(USERS_FILE, users)

                # Add to students.json
                students = load_data(STUDENTS_FILE)
                new_stu_id = max([s["id"] for s in students], default=0) + 1
                new_student = {
                    "id": new_stu_id,
                    "student_id": student_id.upper(),
                    "name": name,
                    "department": department,
                    "email": email,
                    "mobile": mobile,
                    "year": "1st Year",
                    "attendance": 100 # Initial Attendance is 100%
                }
                students.append(new_student)
                save_data(STUDENTS_FILE, students)

                st.success("Registration successful! Redirecting to Login...")
                st.switch_page("pages/Login.py")

    st.markdown("---")
    
    st.page_link("pages/Login.py", label="Already have an account? Sign in here", icon="🔑")

    render_auth_footer()
    st.markdown('</div>', unsafe_allow_html=True)
