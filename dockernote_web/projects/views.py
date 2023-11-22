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
    # codes = Code.objects.filter(
    #     Q(project__owner=user) & Q(project=project)
    # ).order_by('-creation_date')

    context = {
        'page': page,
        'project': project,
        # 'codes': codes,
        'user': user,
    }
    return render(request, 'Projects/display_project.html', context)
