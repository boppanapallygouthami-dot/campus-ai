import streamlit as st

def render_auth_header(title: str, subtitle: str) -> None:
    """Render a premium styled header for login/registration forms."""
    st.markdown(
        f"""
        <div style="text-align: center; margin-bottom: 30px;">
            <h1 style="
                font-size: 2.5em; 
                font-weight: 800; 
                background: linear-gradient(135deg, #60a5fa 0%, #2563eb 100%); 
                -webkit-background-clip: text; 
                -webkit-text-fill-color: transparent;
                margin-bottom: 5px;
            ">
                {title}
            </h1>
            <p style="font-size: 1.1em; opacity: 0.7; margin: 0;">
                {subtitle}
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

def render_auth_footer() -> None:
    """Render small copyright footer on auth pages."""
    st.markdown(
        """
        <div style="text-align: center; margin-top: 40px; font-size: 0.8em; opacity: 0.5;">
            <p>© 2026 Smart Campus Management System. All Rights Reserved.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
