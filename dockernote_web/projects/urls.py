from django.urls import path

from . import views

urlpatterns = [
    path('add_project/', views.addProject, name="add_project"),
    path('display_project/<uuid:project_id>/', views.displayMyProject, name="display_project"),
    path('delete_project/<uuid:project_id>/', views.deleteProject, name="delete_project"),
    path('edit_project/<uuid:project_id>/', views.editProject, name="edit_project"),
    path('add_file/<uuid:project_id>/', views.add_file, name="add_file"),
    path('delete_file/<uuid:project_id>/<str:file_name>/', views.delete_file, name="delete_file"),
    path('run_file/<uuid:project_id>/<str:file_name>/', views.run_file, name="run_file"),
    path('download_file/<uuid:project_id>/<str:file_name>/', views.download_file, name="download_file"),
]
