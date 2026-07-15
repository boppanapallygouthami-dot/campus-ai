import streamlit as st
import config
from utils.database import init_db

# Configure streamlit page parameters
st.set_page_config(
    page_title="Smart Campus Portal",
    page_icon="🏫",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize JSON DB tables
init_db()

# Main entrypoint routing logic
if "authenticated" not in st.session_state or not st.session_state.authenticated:
    st.session_state.current_page = "Login"
    st.switch_page("pages/Login.py")
else:
    st.session_state.current_page = "Dashboard"
    st.switch_page("pages/Dashboard.py")
