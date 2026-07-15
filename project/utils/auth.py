import streamlit as st
import bcrypt
from typing import Dict, List, Optional, Any
from utils.database import USERS_FILE, load_data, save_data

def hash_password(password: str) -> str:
    """Hash password using bcrypt."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")

def verify_password(password: str, hashed: str) -> bool:
    """Verify standard text password against bcrypt hashed value."""
    try:
        return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))
    except Exception:
        return False

def authenticate_user(email: str, password: str) -> Optional[Dict[str, Any]]:
    """Verify user credentials against users.json database."""
    users = load_data(USERS_FILE)
    for user in users:
        if user["email"].lower().strip() == email.lower().strip():
            if verify_password(password, user["password"]):
                return user
    return None

def login_user(user: Dict[str, Any], remember_me: bool = False) -> None:
    """Store user info in session state to authenticate."""
    st.session_state.authenticated = True
    st.session_state.user = {
        "id": user["id"],
        "name": user["name"],
        "student_id": user.get("student_id", ""),
        "department": user.get("department", ""),
        "email": user["email"],
        "mobile": user.get("mobile", ""),
        "role": user["role"]
    }
    st.session_state.remember_me = remember_me
    # Navigate directly to Dashboard after login
    st.switch_page("pages/Dashboard.py")

def logout_user() -> None:
    """Clear user session states and redirect to Login."""
    st.session_state.authenticated = False
    st.session_state.user = None
    if "current_page" in st.session_state:
        del st.session_state.current_page
    st.rerun()

def check_auth(required_roles: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    Ensure user is authenticated and has required role permissions.
    If not authenticated, redirects to Login page.
    If authenticated but role is unauthorized, redirects to Dashboard.
    """
    if "authenticated" not in st.session_state or not st.session_state.authenticated:
        # Redirect to login
        st.warning("Please login to access this page.")
        st.switch_page("pages/Login.py")
        st.stop()
        
    user = st.session_state.user
    if required_roles and user["role"] not in required_roles:
        st.error(f"Unauthorized. This page is only accessible by: {', '.join(required_roles)}")
        st.switch_page("pages/Dashboard.py")
        st.stop()
        
    return user
