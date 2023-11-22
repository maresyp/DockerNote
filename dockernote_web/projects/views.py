import re
import requests
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProjectForm
from .models import Project


@login_required(login_url='login')
def addProject(request):
    """
    This view is used to handle the creation of new projects. It takes a POST request with the new project's information,
    validates it, and if everything checks out, creates a new project and redirects the user to their account page.
    """
    page = 'add_project'

    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            description = form.cleaned_data.get('description')

            if not title:
                form.add_error('title', 'Podaj tytuł dla swojego kodu.')
            elif not description:
                form.add_error('description', 'Dodaj krótki opis o tym czego dotyczy twój kod')
            else:
                new_project = form.save(commit=False)
                new_project.owner = request.user
                new_project.title = title
                new_project.description = description
                new_project.save()

                messages.success(request, 'Projekt został poprawnie utworzony.')
                return redirect('account')
    else:
        form = ProjectForm()

    context = {
        'page': page,
        'form': form,
    }
    return render(request, 'projects/add-edit_project.html', context)

@login_required(login_url='login')
def displayMyProject(request, project_id):
    """
    This view is used to display a specific project's details. It only shows the projects that are owned by the current user.
    If the project is not found or the user is not the owner, a 404 error is raised.
    """
    page = 'display_my_project'
    user = request.user

    project = get_object_or_404(Project, id=project_id)
    mongo_project = requests.get(f'http://file_server:8000/get_project/{project_id}', timeout=10)
    if mongo_project.status_code != 200:
        raise Exception(f'error: {mongo_project.json()["detail"]}')

    mongo_project = mongo_project.json()
    project.title = mongo_project.get('title')
    project.description = mongo_project.get('description')

    context = {
        'page': page,
        'project': project,
        'user': user,
    }
    return render(request, 'projects/display_project.html', context)

@login_required(login_url='login')
def deleteProject(request, project_id):
    """
    This view is used to handle the deletion of an existing project. The user must be the owner of the project to delete it.
    If the user is not the owner, they are redirected to their account page with an error message.
    """
    project = get_object_or_404(Project, id=project_id)

    # check if user is owner of project
    if request.user != project.owner:
        messages.error(request, 'Nie jesteś właścicielem tego projektu.')
        return redirect('account')

    response = requests.delete(f'http://file_server:8000/delete_project/{project_id}', timeout=10)
    if response.status_code != 200:
        messages.error(request, 'Wystąpił problem podczas usuwania projektu.')
        raise Exception(f'error: {response.json()["detail"]}')

    project.delete()
    messages.success(request, 'Projekt został usunięty.')
    return redirect('account')

@login_required(login_url='login')
def editProject(request, project_id):
    """
    This view is used to handle the editing of an existing project. The user must be the owner of the project to edit it.
    If the user is not the owner, they are redirected to their account page with an error message.
    """
    page = 'edit_project'
    project = get_object_or_404(Project, id=project_id)

    if request.user != project.owner:
        messages.error(request, 'Nie jesteś właścicielem tego projektu.')
        return redirect('account')

    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            description = form.cleaned_data.get('description')

            if not title:
                form.add_error('title', 'Podaj tytuł dla swojego projektu.')
            elif not description:
                form.add_error('description', 'Dodaj krótki opis o tym czego dotyczy twój projekt')
            else:
                response = requests.put(f'http://file_server:8000/update_project/{project_id}', json={
                    'title': title,
                    'description': description,
                }, timeout=10)

                if response.status_code != 200:
                    messages.error(request, 'Wystąpił problem podczas edytowania projektu.')
                    raise Exception(f'error: {response.json()["detail"]}')

                messages.success(request, 'Zapisano zmiany.')
    else:
        form = ProjectForm(instance=project)
        response = requests.get(f'http://file_server:8000/get_project/{project_id}', timeout=10)
        if response.status_code != 200:
            raise Exception(f'error: {response.json()["detail"]}')

        mongo_project = response.json()
        form.fields['title'].initial = mongo_project.get('title')
        form.fields['description'].initial = mongo_project.get('description')

    context = {
        'page': page,
        'form': form,
        'project': project,
    }
    return render(request, 'projects/add-edit_project.html', context)

@login_required(login_url='login')
def add_file(request, project_id):
    pass
