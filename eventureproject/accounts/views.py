from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserCreateForm
from events.models import Users, Group as CustomGroup


def home(request):
    if request.user.is_authenticated:
        return redirect('events')
    return redirect('loginaccount')


def signupaccount(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {'form': UserCreateForm()})

    form = UserCreateForm(request.POST)
    if form.is_valid():
        username = form.cleaned_data['username']
        password1 = form.cleaned_data['password1']
        password2 = form.cleaned_data['password2']
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        user_type = form.cleaned_data['user_type']

        if not username.islower():
            return render(request, 'signup.html', {
                'form': form,
                'error': 'Username must be lowercase'
            })

        if password1 != password2:
            return render(request, 'signup.html', {
                'form': form,
                'error': 'Passwords do not match'
            })

        try:
            user = User.objects.create_user (
                username=username,
                password=password1,
                email=email,
                first_name=name
            )

            custom_group, _ = CustomGroup.objects.get_or_create(group_name=user_type)
            Users.objects.create(user=user, group=custom_group)

            login(request, user)
            return redirect('events')

        except IntegrityError:
            return render(request, 'signup.html', {
                'form': form,
                'error': 'Username already taken'
            })

    return render(request, 'signup.html', {
        'form': form,
        'error': 'Invalid form submission'
    })


def loginaccount(request):
    if request.method == 'GET':
        return render(request, 'login.html', {'form': AuthenticationForm()})

    form = AuthenticationForm(request, data=request.POST)
    if form.is_valid():
        login(request, form.get_user())
        return redirect('events')
    else:
        return render(request, 'login.html', {
            'form': form,
            'error': 'Invalid login'
        })


def signoutaccount(request):
    logout(request)
    return redirect('loginaccount')
