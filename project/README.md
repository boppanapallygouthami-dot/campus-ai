# Smart Campus Management System

A complete, production-ready **Smart Campus Management System** built with **Python 3.11+** and **Streamlit**. Featuring a modern SaaS-inspired glassmorphism interface, integrated live/mock weather telemetries, and a secure thread-safe flat file JSON database database.

---

## 🌟 Key Features

* **Authentication & Role-Based Access Control:** Secure session management, bcrypt password hashing, and restricted route validation.
* **Modern SaaS Admin Dashboard:** Key metrics cards, dynamic Plotly visualizations (attendance rate, student demographics, event sign-ups).
* **Flexible Attendance System:** Daily self-checkins for students, date filtering, search filters, and CSV reports generation.
* **Notice Board:** Categorized administrative bulletins with clean text-document downloads.
* **Events Portal:** chronological upcoming activities lists, instant reservation toggles, and detail list exports.
* **Complaints Portal:** Seamless ticketing submission, progress dashboard tracking, and admin triage status updates.
* **Responsive UI Design:** custom CSS with glassmorphism layout, light/dark variables config support, and hidden default navigation overlays.
* **Admin Controls Panel:** Quick student profile creator, editor, notice publisher, and scheduler.

---

## 📂 Folder Structure

```
Smart-Campus/
│
├── app.py                  # Routing manager and app entrypoint
├── config.py               # Environments loader
├── requirements.txt        # PIP dependencies list
├── .env                    # System parameters configurations
├── .env.example            # Environment parameters template
├── README.md               # Overview guidelines documentation
│
├── assets/
│   ├── logo.png            # Smart campus system brand logo
│   ├── background.jpg      # Centered card page backdrop image
│   ├── styles.css          # Customized styles and class variables
│   └── profile_images/     # Uploaded profile files destination
│
├── database/               # JSON Flat-file tables
│   ├── users.json
│   ├── students.json
│   ├── faculty.json
│   ├── attendance.json
│   ├── notices.json
│   ├── events.json
│   └── complaints.json
│
├── components/             # Reusable UI component modules
│   ├── sidebar.py
│   ├── navbar.py
│   ├── cards.py
│   ├── charts.py
│   └── authentication.py
│
├── pages/                  # Route page interfaces
│   ├── Login.py
│   ├── Register.py
│   ├── Dashboard.py
│   ├── Profile.py
│   ├── Attendance.py
│   ├── Notices.py
│   ├── Events.py
│   ├── Complaints.py
│   ├── Settings.py
│   └── Admin.py
│
└── utils/                  # Backend algorithms & calculations
    ├── database.py         # CRUD file actions
    ├── auth.py             # Session and cryptography checks
    ├── validators.py       # Syntax formats checks
    ├── helpers.py          # Data loaders & layout injects
    └── api.py              # Weather REST queries
```

---

## 🚀 Installation & Local Run

### 1. Clone or Copy the Repository
Place the folder structure into your local environment directory.

### 2. Set Up Virtual Environment (Recommended)
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Create and Configure Environment File
Copy `.env.example` to `.env` and fill in active keys (if any). The platform works out-of-the-box with simulated mock data if keys are omitted.
```bash
cp .env.example .env
```

### 5. Launch the Application
```bash
streamlit run app.py
```

---

## 🔑 Default Login Credentials

Use these seeded details to test functionality on the initial run:

* **Administrator Account:**
  - **Email:** `admin@campus.com`
  - **Password:** `Admin@123`
* **Student Account:**
  - **Email:** `student@campus.com`
  - **Password:** `Student@123`

---

## 🔒 Security Practices

1. **Password Safety:** Account passwords are encoded and validated with dynamic salts via the `bcrypt` algorithm.
2. **Session Guards:** Secure redirect functions prevent deep-link access to pages without valid login flags.
3. **Admin Controls:** Middleware validates that user dictionary files contain `"role": "admin"` tags before granting page loads for configuration.

---

## 🛠️ Future Improvements

* **API Integrations:** Support active integrations for Google Classroom, Canvas API, or Microsoft Outlook Schedules.
* **SQL/NoSQL Migration:** Update JSON flat files to PostgreSQL database pools for heavy concurrency loads.
* **Mailing systems:** Configure email notifications via SMTP alerts when complaints change status or notices publish.
