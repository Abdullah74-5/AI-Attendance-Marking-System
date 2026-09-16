# AI-Attendance-Marking-System

---

```markdown
# AI-Powered Face Recognition Attendance System 🚀

A modern, full-stack, enterprise-grade AI Attendance System built with **Django**, **PostgreSQL**, **OpenCV**, and **dlib**. The system features real-time webcam face registration, dynamic video streaming recognition, instant database logging, and an interactive modern dashboard.

---

## 🌟 Key Features

* **Instant Face Registration:** Enrolls students via a webcam snapshot, extracting 128-dimensional facial embeddings using `dlib` / `face_recognition`.
* **Real-Time Recognition Stream:** Live multi-frame webcam feed processing with dynamic bounding boxes and student recognition overlays.
* **Auto-Redirect Confirmation UI:** Displays a smart success modal upon face recognition, counts down 3 seconds, and seamlessly routes back to the dashboard.
* **Enterprise PostgreSQL Integration:** Robust database architecture utilizing PostgreSQL for high concurrency and relational integrity.
* **Clean & Responsive UI:** Built with **Tailwind CSS** for a polished, modern dashboard and scanner view.

---

## 🛠️ Tech Stack

* **Backend:** Python 3.11+, Django 5.x
* **Database:** PostgreSQL
* **Computer Vision & AI:** OpenCV (`cv2`), `dlib`, `face_recognition`, `NumPy`
* **Frontend:** HTML5, JavaScript (Fetch API), Tailwind CSS

---

## 📁 Project Structure

```text
├── detector/
│   ├── models.py          # Student (embeddings) & Attendance database schemas
│   ├── views.py           # Video stream generator, enrollment, & status polling views
│   ├── urls.py            # App route mappings
│   └── templates/
│       └── detector/
│           ├── dashboard.html        # Main analytics & daily attendance log
│           ├── enroll.html           # Student face capture & registration
│           └── mark_attendance.html  # Real-time webcam face scanner
├── attendance_system/     # Core Django configuration
├── manage.py
└── requirements.txt

```

---

## 🚀 Getting Started

### 1. Prerequisites

* **Python 3.11+**
* **PostgreSQL** installed and running on `localhost:5432`
* C++ Build Tools (required for compiling `dlib` binaries if on Windows)

---

### 2. Installation

1. **Clone the repository:**
```bash
git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
cd your-repo-name

```


2. **Create and activate a virtual environment:**
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

```


3. **Install Dependencies:**
```bash
pip install -r requirements.txt

```


> *Note for Windows users:* If you encounter issues installing `dlib`, install `dlib-bin` or pre-compiled wheels, and ensure `setuptools<70` is installed (`pip install "setuptools<70"`).



---

### 3. Database Setup (PostgreSQL)

1. Open PostgreSQL (`psql` or pgAdmin) and create a database named `attendance`:
```sql
CREATE DATABASE attendance;

```


2. Configure your credentials in `attendance_system/settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'attendance',
        'USER': 'postgres',
        'PASSWORD': 'YOUR_POSTGRES_PASSWORD',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

```


3. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate

```



---

### 4. Running the Application

1. Start the Django development server:
```bash
python manage.py runserver

```


2. Open your browser and navigate to:
```text
[http://127.0.0.1:8000/](http://127.0.0.1:8000/)

```



---

## 📖 How to Use

1. **Dashboard (`/`):** Displays total registered students, today's attendance count, and live timestamp logs.
2. **Student Enrollment (`/enroll/`):** Enter student name and Roll Number/ID. Allow webcam access, then click **Capture & Register Face**.
3. **Mark Attendance (`/mark-attendance/`):** Look directly at the live camera scanner. Once recognized:
* Attendance is instantly recorded in PostgreSQL.
* A confirmation screen pops up showing the student's name.
* Automatically redirects to the main dashboard after 3 seconds.



---

## 🔮 Future Roadmap

* [ ] Anti-spoofing / Blink detection (Liveness verification).
* [ ] Vector database optimization using `pgvector` for scaling to thousands of faces.
* [ ] Export attendance logs to CSV/PDF reports.
* [ ] Django REST Framework (DRF) endpoints for mobile app integrations.

```

```
