import streamlit as st
import utils.auth as auth
import utils.validators as val
from components.authentication import render_auth_header, render_auth_footer
from utils.helpers import load_css
from pathlib import Path
import base64

# Page configurations
st.set_page_config(page_title="Login - Smart Campus", page_icon="🔑", layout="centered")

# Load styles.css
load_css()

# Track page path
st.session_state.current_page = "Login"

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

# Outer centered container for glassmorphic card
with st.container():
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    
    render_auth_header("Smart Campus", "Please sign in to access your portal")

    # Form parameters
    email = st.text_input("Campus Email Address", placeholder="e.g. name@campus.com")
    password = st.text_input("Password", type="password", placeholder="Enter your password")
    
    col_left, col_right = st.columns([1, 1])
    with col_left:
        remember_me = st.checkbox("Remember Me", value=False)
    with col_right:
        forgot_password = st.button("Forgot Password?", key="btn_forgot", help="Click to simulate password reset")
        if forgot_password:
            st.info("💡 Passwords can be reset via the Admin panel or database/users.json file directly.")

    st.markdown("<br>", unsafe_allow_html=True)
    
    login_submitted = st.button("Log In")

    if login_submitted:
        # Validation checks
        if not email or not password:
            st.error("Please fill in all the fields.")
        elif not val.validate_email(email):
            st.error("Invalid email address format.")
        else:
            # Attempt authentication
            user = auth.authenticate_user(email, password)
            if user:
                # Directly navigate to Dashboard — no st.success needed here
                # because st.switch_page is called inside login_user()
                auth.login_user(user, remember_me)
            else:
                st.error("Incorrect email or password. Please try again.")

    st.markdown("---")
    
    st.page_link("pages/Register.py", label="Don't have an account? Register here", icon="📝")

    render_auth_footer()
    st.markdown('</div>', unsafe_allow_html=True)
