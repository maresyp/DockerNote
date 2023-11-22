from django.urls import path

from . import views

urlpatterns = [
    path('add_project/', views.addProject, name="add_project"),
    path('display_project/<uuid:project_id>/', views.displayMyProject, name="display_project"),
]
