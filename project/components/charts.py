import streamlit as st
import plotly.express as px
import pandas as pd
from typing import List, Dict, Any

def render_attendance_chart(attendance_data: List[Dict[str, Any]]) -> None:
    """Render attendance line graph over dates using Plotly."""
    if not attendance_data:
        st.info("No attendance records available for charting.")
        return

    df = pd.DataFrame(attendance_data)
    
    # Calculate % present for each date
    df['is_present'] = df['status'].apply(lambda x: 1 if x == 'Present' else 0)
    summary = df.groupby('date')['is_present'].mean().reset_index()
    summary['Percentage'] = (summary['is_present'] * 100).round(1)

    fig = px.line(
        summary, 
        x='date', 
        y='Percentage', 
        title='Average Campus Attendance Rate (%)',
        markers=True,
        labels={'date': 'Date', 'Percentage': 'Attendance Rate (%)'}
    )
    
    # Update styling to match dark SaaS theme
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)'),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', range=[0, 105]),
        margin=dict(l=40, r=40, t=40, b=40)
    )
    st.plotly_chart(fig, use_container_width=True)

def render_department_chart(student_data: List[Dict[str, Any]]) -> None:
    """Render distribution of students across departments using a Donut chart."""
    if not student_data:
        st.info("No student records available for department charting.")
        return

    df = pd.DataFrame(student_data)
    dept_counts = df['department'].value_counts().reset_index()
    dept_counts.columns = ['Department', 'Count']

    fig = px.pie(
        dept_counts, 
        values='Count', 
        names='Department', 
        title='Student Distribution by Department',
        hole=0.4
    )
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        margin=dict(l=40, r=40, t=40, b=40)
    )
    st.plotly_chart(fig, use_container_width=True)

def render_monthly_activities(events_data: List[Dict[str, Any]]) -> None:
    """Render events bar chart showing registrations/attendees."""
    if not events_data:
        st.info("No event records available.")
        return

    events_summary = []
    for item in events_data:
        events_summary.append({
            "Event": item.get("event", "Event"),
            "Attendees": len(item.get("attendees", []))
        })
    df = pd.DataFrame(events_summary)

    fig = px.bar(
        df, 
        x='Event', 
        y='Attendees', 
        title='Event Registration Counts',
        labels={'Attendees': 'Number of Registrations'}
    )
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)'),
        margin=dict(l=40, r=40, t=40, b=40)
    )
    st.plotly_chart(fig, use_container_width=True)
