import json
import os
from pathlib import Path
from typing import Dict, List, Any
import bcrypt
import config

# Paths for JSON files
USERS_FILE = config.DATABASE_PATH / "users.json"
STUDENTS_FILE = config.DATABASE_PATH / "students.json"
FACULTY_FILE = config.DATABASE_PATH / "faculty.json"
ATTENDANCE_FILE = config.DATABASE_PATH / "attendance.json"
NOTICES_FILE = config.DATABASE_PATH / "notices.json"
EVENTS_FILE = config.DATABASE_PATH / "events.json"
COMPLAINTS_FILE = config.DATABASE_PATH / "complaints.json"

def init_db() -> None:
    """Initialize JSON database files with default data if missing."""
    config.DATABASE_PATH.mkdir(parents=True, exist_ok=True)
    
    # Helper to hash passwords dynamically during seed
    def hash_pwd(pwd: str) -> str:
        return bcrypt.hashpw(pwd.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    # 1. Initialize users.json
    if not USERS_FILE.exists():
        default_users = [
            {
                "id": 1,
                "name": "Admin User",
                "student_id": "ADMIN001",
                "department": "Administration",
                "email": "admin@campus.com",
                "mobile": "1234567890",
                "password": hash_pwd("Admin@123"),
                "role": "admin"
            },
            {
                "id": 2,
                "name": "John Doe",
                "student_id": "STU001",
                "department": "Computer Science",
                "email": "student@campus.com",
                "mobile": "9876543210",
                "password": hash_pwd("Student@123"),
                "role": "student"
            }
        ]
        save_data(USERS_FILE, default_users)

    # 2. Initialize students.json
    if not STUDENTS_FILE.exists():
        default_students = [
            {
                "id": 1,
                "student_id": "STU001",
                "name": "John Doe",
                "department": "Computer Science",
                "email": "student@campus.com",
                "mobile": "9876543210",
                "year": "3rd Year",
                "attendance": 95
            }
        ]
        save_data(STUDENTS_FILE, default_students)

    # 3. Initialize faculty.json
    if not FACULTY_FILE.exists():
        default_faculty = [
            {
                "id": 1,
                "faculty_id": "FAC001",
                "name": "Dr. Alan Turing",
                "department": "Computer Science",
                "email": "turing@campus.com",
                "mobile": "5551234567"
            }
        ]
        save_data(FACULTY_FILE, default_faculty)

    # 4. Initialize attendance.json
    if not ATTENDANCE_FILE.exists():
        default_attendance = [
            {
                "student_id": "STU001",
                "date": "2026-07-10",
                "status": "Present"
            },
            {
                "student_id": "STU001",
                "date": "2026-07-11",
                "status": "Present"
            },
            {
                "student_id": "STU001",
                "date": "2026-07-12",
                "status": "Present"
            },
            {
                "student_id": "STU001",
                "date": "2026-07-13",
                "status": "Absent"
            },
            {
                "student_id": "STU001",
                "date": "2026-07-14",
                "status": "Present"
            }
        ]
        save_data(ATTENDANCE_FILE, default_attendance)

    # 5. Initialize notices.json
    if not NOTICES_FILE.exists():
        default_notices = [
            {
                "id": 1,
                "title": "Semester Exams Schedule Released",
                "description": "The semester end exams are scheduled to start from August 10, 2026. Please collect your admit cards.",
                "category": "Academics",
                "date": "2026-07-14"
            },
            {
                "id": 2,
                "title": "Annual Hackathon Registrations Open",
                "description": "Register for the Campus Hackathon 2026. Cash prizes up to $5000.",
                "category": "Events",
                "date": "2026-07-12"
            }
        ]
        save_data(NOTICES_FILE, default_notices)

    # 6. Initialize events.json
    if not EVENTS_FILE.exists():
        default_events = [
            {
                "id": 1,
                "event": "Smart Campus Tech Fest",
                "venue": "Main Seminar Hall",
                "date": "2026-08-20",
                "description": "A day showcasing student engineering projects, coding tournaments, and expert tech talks.",
                "attendees": ["STU001"]
            },
            {
                "id": 2,
                "event": "Alumni Networking Summit",
                "venue": "Campus Auditorium",
                "date": "2026-09-05",
                "description": "Meet and connect with successful alumni working in top tech companies worldwide.",
                "attendees": []
            }
        ]
        save_data(EVENTS_FILE, default_events)

    # 7. Initialize complaints.json
    if not COMPLAINTS_FILE.exists():
        default_complaints = [
            {
                "id": 1,
                "student_id": "STU001",
                "student": "John Doe",
                "issue": "WiFi signal strength is very low in Hostel Block B, room 305.",
                "status": "In Progress",
                "date": "2026-07-13"
            }
        ]
        save_data(COMPLAINTS_FILE, default_complaints)

def load_data(filepath: Path) -> List[Dict[str, Any]]:
    """Load JSON data from file with exception handling."""
    if not filepath.exists():
        return []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error reading JSON file {filepath}: {e}")
        return []

def save_data(filepath: Path, data: List[Dict[str, Any]]) -> bool:
    """Save JSON data to file safely."""
    try:
        # Save to temp file first, then rename to ensure atomic write
        temp_filepath = filepath.with_suffix(".tmp")
        with open(temp_filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        temp_filepath.replace(filepath)
        return True
    except IOError as e:
        print(f"Error writing to JSON file {filepath}: {e}")
        return False

# Initialize database on module load
init_db()
