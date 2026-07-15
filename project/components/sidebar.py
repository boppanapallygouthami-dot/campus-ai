import streamlit as st
from streamlit_option_menu import option_menu
import utils.auth as auth
from pathlib import Path
from PIL import Image

def render_sidebar() -> None:
    """Render the custom sidebar with user info and page links."""
    # Ensure user is logged in
    if "user" not in st.session_state or st.session_state.user is None:
        return

    user = st.session_state.user
    role = user.get("role", "student")

    with st.sidebar:
        # Load and render campus logo
        logo_path = Path(__file__).resolve().parent.parent / "assets" / "logo.png"
        if logo_path.exists():
            try:
                logo_img = Image.open(logo_path)
                st.image(logo_img, use_column_width=True)
            except Exception:
                st.markdown("### 🏫 Smart Campus")
        else:
            st.markdown("### 🏫 Smart Campus")

        st.markdown("---")

        # Display logged-in user profile snippet
        st.markdown(
            f"""
            <div style="text-align: center; margin-bottom: 20px; padding: 10px; background: rgba(255,255,255,0.05); border-radius: 10px;">
                <p style="margin: 0; font-size: 1.1em; font-weight: 600; color: #4a90e2;">{user.get('name', 'User')}</p>
                <p style="margin: 0; font-size: 0.85em; opacity: 0.7;">{user.get('email', '')}</p>
                <span style="display: inline-block; margin-top: 5px; padding: 2px 8px; font-size: 0.75em; border-radius: 12px; background: #357abd; color: white;">{role.upper()}</span>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Define menu items based on role
        menu_options = ["Dashboard", "Profile", "Attendance", "Notices", "Events", "Complaints", "Settings"]
        menu_icons = ["speedometer2", "person-badge-fill", "calendar-check-fill", "file-earmark-text-fill", "calendar-event-fill", "exclamation-triangle-fill", "gear-fill"]

        if role == "admin":
            menu_options.append("Admin Panel")
            menu_icons.append("shield-lock-fill")

        menu_options.append("Logout")
        menu_icons.append("box-arrow-right")

        # Determine default active menu item index
        active_page = st.session_state.get("current_page", "Dashboard")
        default_index = 0
        if active_page in menu_options:
            default_index = menu_options.index(active_page)

        # Render streamlit-option-menu
        selected = option_menu(
            menu_title="Main Navigation",
            options=menu_options,
            icons=menu_icons,
            menu_icon="cast",
            default_index=default_index,
            styles={
                "container": {"padding": "5px", "background-color": "transparent"},
                "icon": {"color": "#4a90e2", "font-size": "16px"}, 
                "nav-link": {"font-size": "14px", "text-align": "left", "margin": "0px", "--hover-color": "rgba(74, 144, 226, 0.1)"},
                "nav-link-selected": {"background-color": "#4a90e2"},
            }
        )

        # Navigation routing logic
        if selected == "Logout":
            auth.logout_user()
        elif selected != active_page:
            # Map selection to file paths
            page_mapping = {
                "Dashboard": "pages/Dashboard.py",
                "Profile": "pages/Profile.py",
                "Attendance": "pages/Attendance.py",
                "Notices": "pages/Notices.py",
                "Events": "pages/Events.py",
                "Complaints": "pages/Complaints.py",
                "Settings": "pages/Settings.py",
                "Admin Panel": "pages/Admin.py"
            }
            if selected in page_mapping:
                st.session_state.current_page = selected
                st.switch_page(page_mapping[selected])
