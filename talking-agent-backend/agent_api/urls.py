from django.urls import path
from . import views

urlpatterns = [
    path('process-voice/', views.ProcessVoiceView.as_view(), name='process_voice'),
    path('health/', views.HealthCheckView.as_view(), name='health_check'),
    path('credits/', views.CheckCreditsView.as_view(), name='check_credits'),
]