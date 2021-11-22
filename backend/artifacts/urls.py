from django.urls import path
from . import views

urlpatterns = [
    path('museum/<str:museum_name>/', views.get_museum_info),
    path('<str:artifact_id>/', views.artifact_detail),
    path('<str:artifact_id>/like/', views.artifact_like),
    path('<str:artifact_id>/resemble/', views.artifact_resemble),
    path('<str:artifact_id>/wordcloud/', views.wordcloud),
]