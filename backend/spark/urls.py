from django.urls import path
from . import views

urlpatterns = [
    path('userface/', views.user_face),
]