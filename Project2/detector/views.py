# detector/views.py
import cv2
import json
import base64
import numpy as np
import face_recognition
from PIL import Image
from io import BytesIO

from django.shortcuts import render
from django.http import JsonResponse, StreamingHttpResponse
from django.utils import timezone
from .models import Student, Attendance

# --- 1. DASHBOARD VIEW ---
def dashboard(request):
    today = timezone.now().date()
    total_students = Student.objects.count()
    today_attendance = Attendance.objects.filter(date=today)
    present_count = today_attendance.count()
    
    context = {
        'total_students': total_students,
        'present_count': present_count,
        'attendance_records': today_attendance,
        'today_date': today,
    }
    return render(request, 'detector/dashboard.html', context)

# --- ENROLLMENT VIEW ---
def enroll_student(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name')
            roll_number = data.get('roll_number')
            image_data = data.get('image')

            if not image_data or ';base64,' not in image_data:
                return JsonResponse({'status': 'error', 'message': 'No image snapshot received.'})

            # 1. Decode base64 to OpenCV image array
            imgstr = image_data.split(';base64,')[1]
            img_bytes = base64.b64decode(imgstr)
            np_arr = np.frombuffer(img_bytes, dtype=np.uint8)
            bgr_frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

            if bgr_frame is None:
                return JsonResponse({'status': 'error', 'message': 'Corrupted image received. Please try again!'})

            # 2. Convert BGR -> RGB
            rgb_frame = cv2.cvtColor(bgr_frame, cv2.COLOR_BGR2RGB)

            # 3. FORCE STRICT DLIB-COMPATIBLE MEMORY LAYOUT (Fixes NumPy 2.x / dlib flag mismatches)
            clean_rgb_frame = np.array(rgb_frame, dtype=np.uint8, copy=True, order='C')

            # 4. Detect faces
            face_locations = face_recognition.face_locations(clean_rgb_frame)
            if not face_locations:
                return JsonResponse({'status': 'error', 'message': 'No face detected in capture. Ensure good lighting!'})

            encodings = face_recognition.face_encodings(clean_rgb_frame, face_locations)
            embedding_list = encodings[0].tolist()

            # 5. Save record to SQLite
            student, created = Student.objects.update_or_create(
                roll_number=roll_number,
                defaults={'name': name, 'face_embedding': embedding_list}
            )

            return JsonResponse({'status': 'success', 'message': f'Student {name} registered successfully!'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return render(request, 'detector/enroll.html')

# --- 3. LIVE ATTENDANCE STREAM & ENGINE ---
def gen_attendance_frames():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    while True:
        success, frame = cap.read()
        if not success:
            break

        # Convert BGR to RGB for face_recognition
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        # Query all enrolled student embeddings from database
        students = Student.objects.exclude(face_embedding__isnull=True)
        known_encodings = [np.array(s.face_embedding) for s in students]
        known_students = list(students)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            name = "Unknown"
            color = (0, 0, 255) # Red for unrecognised faces

            if known_encodings:
                # Calculate Euclidean distance against all known vectors
                distances = face_recognition.face_distance(known_encodings, face_encoding)
                best_match_index = np.argmin(distances)

                # Threshold 0.5 for accurate matching
                if distances[best_match_index] < 0.5:
                    student = known_students[best_match_index]
                    name = f"{student.name} ({student.roll_number})"
                    color = (0, 255, 0) # Green for match

                    # Log today's attendance in database automatically
                    today = timezone.now().date()
                    Attendance.objects.get_or_create(student=student, date=today)

            # Draw bounding box and name tag
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            cv2.rectangle(frame, (left, bottom - 25), (right, bottom), color, cv2.FILLED)
            cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255), 1)

        ret, buffer = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

    cap.release()

def mark_attendance_page(request):
    return render(request, 'detector/mark_attendance.html')

def video_feed_attendance(request):
    return StreamingHttpResponse(
        gen_attendance_frames(),
        content_type='multipart/x-mixed-replace; boundary=frame'
    )
    
from django.utils import timezone
from django.http import JsonResponse
from datetime import datetime
from .models import Attendance

def check_latest_attendance(request):
    """Returns true only if attendance was marked AFTER the live page was opened."""
    session_start_str = request.GET.get('session_start')
    
    if not session_start_str:
        return JsonResponse({'marked': False})

    try:
        # Parse ISO timestamp sent from browser
        session_start = datetime.fromisoformat(session_start_str.replace('Z', '+00:00'))
        
        # Query attendance marked after session started
        recent_log = Attendance.objects.select_related('student').filter(
            date=timezone.now().date(),
            created_at__gte=session_start  # Ensures we only match NEW detections
        ).order_by('-time').first()

        if recent_log:
            return JsonResponse({
                'marked': True,
                'student_name': recent_log.student.name
            })
    except Exception as e:
        pass

    return JsonResponse({'marked': False})