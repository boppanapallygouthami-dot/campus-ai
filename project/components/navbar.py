import streamlit as st
from utils.api import fetch_weather_data

def render_navbar(page_title: str) -> None:
    """Render a premium styled campus navigation/info header at the top of pages."""
    weather = fetch_weather_data()
    
    weather_html = ""
    if weather.get("success", False):
        weather_html = f"""
        <div style="font-size: 0.9em; text-align: right;">
            <span style="color: #4a90e2; font-weight: 600;">⛅ {weather['city']}:</span> 
            <span>{weather['temp']}°C, {weather['condition']}</span>
            <span style="font-size: 0.8em; opacity: 0.6; display: block;">{weather['source']}</span>
        </div>
        """
    else:
        weather_html = f"""
        <div style="font-size: 0.9em; text-align: right; opacity: 0.6;">
            <span>⛅ Weather Offline</span>
        </div>
        """

    # Custom Header layout
    st.markdown(
        f"""
        <div style="
            display: flex; 
            justify-content: space-between; 
            align-items: center; 
            background: rgba(30, 41, 59, 0.7); 
            backdrop-filter: blur(12px); 
            border: 1px solid rgba(255, 255, 255, 0.1); 
            padding: 15px 25px; 
            border-radius: 12px; 
            margin-bottom: 25px;
            box-shadow: 0 4px 15px 0 rgba(0, 0, 0, 0.1);
        ">
            <div>
                <h2 style="margin: 0; font-size: 1.6em; font-weight: 700; background: linear-gradient(135deg, #fff 0%, #a5b4fc 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                    {page_title}
                </h2>
                <span style="font-size: 0.8em; opacity: 0.6;">Smart Campus Management Portal</span>
            </div>
            {weather_html}
        </div>
        """,
        unsafe_allow_html=True
    )
