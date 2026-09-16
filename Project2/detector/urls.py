# detector/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('enroll/', views.enroll_student, name='enroll'),
    path('mark-attendance/', views.mark_attendance_page, name='mark_attendance'),
    path('video-feed-attendance/', views.video_feed_attendance, name='video_feed_attendance'),
    path('check-latest-attendance/', views.check_latest_attendance, name='check_latest_attendance'),
]
