import streamlit as st
import utils.auth as auth
import utils.validators as val
from components.sidebar import render_sidebar
from components.navbar import render_navbar
from utils.helpers import load_css
from utils.database import load_data, save_data, USERS_FILE, STUDENTS_FILE
from pathlib import Path
from PIL import Image

# Set page config
st.set_page_config(page_title="My Profile - Smart Campus", page_icon="👤", layout="wide")

# Load CSS
load_css()

# Track page path
st.session_state.current_page = "Profile"

# Enforce auth
user = auth.check_auth()

render_sidebar()
render_navbar("User Profile Management")

# Define target paths for profile image upload
UPLOAD_DIR = Path(__file__).resolve().parent.parent / "assets" / "profile_images"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# Fetch user details
users = load_data(USERS_FILE)
students = load_data(STUDENTS_FILE)

# Current user's index in lists
user_idx = next((i for i, u in enumerate(users) if u["id"] == user["id"]), None)

st.markdown('<div class="glass-card">', unsafe_allow_html=True)
col_left, col_right = st.columns([1, 2])

with col_left:
    st.markdown("### 📷 Profile Image")
    
    # Render profile image if it exists, otherwise default placeholder
    img_name = f"profile_{user['id']}.png"
    img_path = UPLOAD_DIR / img_name
    
    if img_path.exists():
        try:
            profile_img = Image.open(img_path)
            st.image(profile_img, width=200, caption="Current Profile Photo")
        except Exception:
            st.info("👤 Placeholder Image")
    else:
        st.markdown(
            """
            <div style="
                width: 200px; 
                height: 200px; 
                border-radius: 50%; 
                background: #357abd; 
                color: white; 
                font-size: 5em; 
                display: flex; 
                justify-content: center; 
                align-items: center; 
                margin-bottom: 15px;
                box-shadow: 0 4px 15px 0 rgba(0, 0, 0, 0.2);
            ">
                👤
            </div>
            """,
            unsafe_allow_html=True
        )
        
    # File Uploader
    uploaded_file = st.file_uploader("Upload New Image (PNG/JPG)", type=["png", "jpg", "jpeg"])
    if uploaded_file is not None:
        try:
            img = Image.open(uploaded_file)
            img.save(img_path)
            st.success("🎉 Image uploaded successfully!")
            st.rerun()
        except Exception as e:
            st.error(f"Error saving image: {e}")

with col_right:
    st.markdown("### 📝 Edit Personal Details")
    
    # Load user's record from JSON
    if user_idx is not None:
        user_record = users[user_idx]
        
        with st.form("profile_update_form"):
            new_name = st.text_input("Full Name", value=user_record.get("name", ""))
            new_mobile = st.text_input("Mobile Number (10 digits)", value=user_record.get("mobile", ""))
            
            # Department select box
            depts = ["Computer Science", "Electrical Engineering", "Mechanical Engineering", "Civil Engineering", "Business Administration", "Physics", "Administration"]
            dept_idx = depts.index(user_record.get("department", "Computer Science")) if user_record.get("department") in depts else 0
            new_dept = st.selectbox("Department", options=depts, index=dept_idx)
            
            st.text_input("Email Address (Locked)", value=user_record.get("email", ""), disabled=True)
            if user_record.get("role") == "student":
                st.text_input("Student ID (Locked)", value=user_record.get("student_id", ""), disabled=True)
                
            update_submitted = st.form_submit_button("Update Profile Info")
            
            if update_submitted:
                if not new_name or not new_mobile:
                    st.error("Fields cannot be empty.")
                elif not val.validate_mobile(new_mobile):
                    st.error("Mobile number must be exactly 10 digits.")
                else:
                    # Update users.json
                    user_record["name"] = new_name
                    user_record["mobile"] = new_mobile
                    user_record["department"] = new_dept
                    save_data(USERS_FILE, users)
                    
                    # Update students.json if applicable
                    if user_record.get("role") == "student":
                        for s in students:
                            if s["student_id"] == user_record.get("student_id"):
                                s["name"] = new_name
                                s["mobile"] = new_mobile
                                s["department"] = new_dept
                        save_data(STUDENTS_FILE, students)
                        
                    # Update local session state
                    st.session_state.user["name"] = new_name
                    st.session_state.user["mobile"] = new_mobile
                    st.session_state.user["department"] = new_dept
                    
                    st.success("🎉 Profile information updated successfully!")
                    st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# 3. Change Password Section
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.subheader("🔐 Change Account Password")

with st.form("change_password_form"):
    curr_pwd = st.text_input("Current Password", type="password")
    new_pwd = st.text_input("New Password", type="password", help="Must be strong password (uppercase, lowercase, numbers, special symbols)")
    confirm_pwd = st.text_input("Confirm New Password", type="password")
    
    password_submitted = st.form_submit_button("Change Password")
    
    if password_submitted:
        if not curr_pwd or not new_pwd or not confirm_pwd:
            st.error("Please fill in all password fields.")
        elif new_pwd != confirm_pwd:
            st.error("New passwords do not match.")
        elif not val.validate_password(new_pwd):
            st.error("New password does not meet strength rules (needs letters, digits, specials, minimum 8 characters).")
        else:
            if user_idx is not None:
                user_record = users[user_idx]
                if not auth.verify_password(curr_pwd, user_record["password"]):
                    st.error("Current password is incorrect.")
                else:
                    # Re-hash and save
                    user_record["password"] = auth.hash_password(new_pwd)
                    save_data(USERS_FILE, users)
                    st.success("🎉 Password updated successfully!")
st.markdown('</div>', unsafe_allow_html=True)
