from django.urls import path
from . import views

urlpatterns = [
    path('recommend/', views.artifact_recommend),
    path('saverecommend/<int:pageNo>', views.artifact_save_recommend),

]