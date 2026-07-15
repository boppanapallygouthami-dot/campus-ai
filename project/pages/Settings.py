import streamlit as st
import utils.auth as auth
from components.sidebar import render_sidebar
from components.navbar import render_navbar
from utils.helpers import load_css

# Page configurations
st.set_page_config(page_title="Settings - Smart Campus", page_icon="⚙️", layout="wide")

# Theme setup in session state if not present
if "theme" not in st.session_state:
    st.session_state.theme = "Dark"

# Load styles
load_css()

# Track page path
st.session_state.current_page = "Settings"

# Enforce auth
user = auth.check_auth()

render_sidebar()
render_navbar("System Settings")

st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.subheader("🎨 Display Theme Configurator")
st.write("Toggle the visual theme layout of your Smart Campus interface.")

# Theme selector
theme_opts = ["Dark", "Light"]
active_theme_idx = theme_opts.index(st.session_state.theme)

selected_theme = st.radio(
    "Choose Color Theme",
    options=theme_opts,
    index=active_theme_idx,
    horizontal=True,
    help="Select 'Light' to enable modern light layout variables, or 'Dark' for SaaS neon layouts."
)

if selected_theme != st.session_state.theme:
    st.session_state.theme = selected_theme
    st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# Notifications Section
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.subheader("🔔 Notification Preferences")
st.write("Choose what channels and events trigger notifications in your dashboard feed.")

if "notif_academics" not in st.session_state:
    st.session_state.notif_academics = True
if "notif_events" not in st.session_state:
    st.session_state.notif_events = True
if "notif_complaints" not in st.session_state:
    st.session_state.notif_complaints = False

notif_acad = st.checkbox("Academic & Schedule Updates", value=st.session_state.notif_academics, help="Recieve alerts for exam updates and academic notifications.")
notif_evts = st.checkbox("Campus Activity & Event Alerts", value=st.session_state.notif_events, help="Recieve reminders for registered and upcoming tech festivals and summits.")
notif_comp = st.checkbox("Complaint Ticket Status Alerts", value=st.session_state.notif_complaints, help="Get status alerts for resolved complaint portal tickets.")

if (notif_acad != st.session_state.notif_academics or 
    notif_evts != st.session_state.notif_events or 
    notif_comp != st.session_state.notif_complaints):
    st.session_state.notif_academics = notif_acad
    st.session_state.notif_events = notif_evts
    st.session_state.notif_complaints = notif_comp
    st.success("Notification preferences updated successfully.")
    
st.markdown('</div>', unsafe_allow_html=True)

# System and Account logout section
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.subheader("💻 System Information")
st.markdown(
    """
    <div style="font-size: 0.9em; opacity: 0.8; line-height: 1.6;">
        <strong>Platform version:</strong> v1.0.0 (Production Ready)<br>
        <strong>Database type:</strong> JSON Flat File Database (Thread-safe atomic locks)<br>
        <strong>Environment:</strong> Python Streamlit Engine
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("<br>", unsafe_allow_html=True)
if st.button("🚪 Logout of Account"):
    auth.logout_user()
    
st.markdown('</div>', unsafe_allow_html=True)
