from django.urls import path
from . import views

urlpatterns = [
    path('', views.api, name='api'),
    path('doctor/', views.DoctorView.as_view(), name='doctor'),
    path('doctor/<int:pk>/', views.DoctorView.as_view(), name='doctor_detail'),
    path('doctor/<int:pk>/exercises/', views.DoctorView.as_view(), name='doctor_exercises'),
    path('patient/', views.PatientView.as_view(), name='patient'),
    path('patient/<int:pk>/', views.PatientView.as_view(), name='patient_detail'),
    path('patient/<int:pk>/exercises/', views.PatientView.as_view(), name='patient_exercises'),
    path('exercise/', views.ExerciseView.as_view(), name='exercise'),
    path('exercise/<int:pk>/', views.ExerciseView.as_view(), name='exercise_detail'),
]