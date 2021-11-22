from django.urls import path
from . import views

urlpatterns = [
    path('<str:artifact_id>/', views.artifact_detail),
]