import streamlit as st
from typing import Dict, Any

def render_metric_cards(stats: Dict[str, Any]) -> None:
    """
    Render key campus performance metrics in responsive glassmorphic cards.
    Accepts stats dict with keys:
    - total_students, total_faculty, attendance_pct, active_events, total_notices, total_complaints
    """
    
    col1, col2, col3 = st.columns(3)
    col4, col5, col6 = st.columns(3)

    metrics = [
        {"title": "Total Students", "value": stats.get("total_students", 0), "icon": "👥", "color": "linear-gradient(135deg, #3b82f6, #1d4ed8)", "col": col1},
        {"title": "Total Faculty", "value": stats.get("total_faculty", 0), "icon": "🎓", "color": "linear-gradient(135deg, #10b981, #047857)", "col": col2},
        {"title": "Attendance Rate", "value": f"{stats.get('attendance_pct', 0.0)}%", "icon": "📅", "color": "linear-gradient(135deg, #f59e0b, #d97706)", "col": col3},
        {"title": "Active Events", "value": stats.get("active_events", 0), "icon": "🏆", "color": "linear-gradient(135deg, #8b5cf6, #6d28d9)", "col": col4},
        {"title": "Notices", "value": stats.get("total_notices", 0), "icon": "📢", "color": "linear-gradient(135deg, #ec4899, #be185d)", "col": col5},
        {"title": "Pending Issues", "value": stats.get("total_complaints", 0), "icon": "⚠️", "color": "linear-gradient(135deg, #ef4444, #b91c1c)", "col": col6}
    ]

    for item in metrics:
        with item["col"]:
            st.markdown(
                f"""
                <div style="
                    background: rgba(30, 41, 59, 0.65);
                    border: 1px solid rgba(255, 255, 255, 0.08);
                    border-radius: 16px;
                    padding: 20px;
                    margin-bottom: 20px;
                    box-shadow: 0 4px 15px 0 rgba(0, 0, 0, 0.1);
                    text-align: center;
                    transition: transform 0.3s ease;
                ">
                    <div style="
                        display: inline-flex;
                        justify-content: center;
                        align-items: center;
                        width: 50px;
                        height: 50px;
                        border-radius: 50%;
                        background: {item['color']};
                        color: white;
                        font-size: 1.5em;
                        margin-bottom: 12px;
                    ">
                        {item['icon']}
                    </div>
                    <h3 style="margin: 0; font-size: 2.2em; font-weight: 800; color: white;">{item['value']}</h3>
                    <p style="margin: 5px 0 0 0; font-size: 0.9em; opacity: 0.7; font-weight: 500;">{item['title']}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
