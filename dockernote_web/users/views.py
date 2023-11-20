from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count, F, Min, OuterRef, Q, Subquery
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import (
    ChangePasswordForm,
    CustomUserCreationForm,
    ProfileForm,
)

# Create your views here.

def loginUser(request):
    """
    Login a user.

    :param request: A Django HttpRequest object.
    :type request: django.http.HttpRequest
    :returns:  A Django HttpResponse object.
    :rtype: django.http.HttpResponse
    """
    page = 'login'

    if request.user.is_authenticated:
        return redirect('account')

    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, 'Nie istnieje użytkownik o podanej nazwie.')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # Profile.objects.filter(user=user.id).update(is_active=True)
            return redirect(request.GET['next'] if 'next' in request.GET else 'account')

        messages.error(request, 'Nazwa użytkownika lub hasło jest niepoprawne.')

    context = {'page': page}
    return render(request, 'users/login_register.html', context)


def logoutUser(request):
    """
    Logout a user.

    :param request: A Django HttpRequest object.
    :type request: django.http.HttpRequest
    :returns:  A Django HttpResponse object.
    :rtype: django.http.HttpResponse
    """
    # Get logged in user
    user = request.user

    # Update user status
    # Profile.objects.filter(user=user.id).update(is_active=False)

    logout(request)
    messages.info(request, 'Pomyślnie wylogowano!')
    return redirect('login')


def registerUser(request):
    """
    Register a new user.

    :param request: A Django HttpRequest object.
    :type request: django.http.HttpRequest
    :returns:  A Django HttpResponse object.
    :rtype: django.http.HttpResponse
    """
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username'].lower()
            email = form.cleaned_data['email'].lower()

            user = form.save(commit=False)
            user.username = user.username.lower()
            user.email = user.email.lower()

            # Check if user with the same username or email already exists
            if User.objects.filter(email=email).exists():
                form.add_error('email', 'Ten adres email jest już w użyciu.')
            elif User.objects.filter(username=username).exists():
                form.add_error('username', 'Użytkownik o takiej nazwie już istnieje.')
            else:
                user.save()
                messages.success(request, 'Konto użytkownika zostało utworzone!')
                login(request, user)
                return redirect('account')
        else:
            messages.error(
                request, 'Wystąpił problem podczas rejestracji')

    context = {'page': page, 'form': form}
    return render(request, 'users/login_register.html', context)
