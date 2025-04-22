from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserCreateForm
from events.models import Users, Group as CustomGroup

def home(request):
    if request.user.is_authenticated:
        # If user is logged in, redirect to the events.html
        return redirect('events')
     # If not logged in, redirect to login.html
    return redirect('loginaccount')


def signupaccount(request):
    # If request method is GET, show an empty sign-up form
    if request.method == 'GET':
        # If request method is POST, process the form data and go to signup.html
        return render(request, 'signup.html', {'form': UserCreateForm()})

    form = UserCreateForm(request.POST)
    # If the form is valid proceed
    if form.is_valid():
        # get the input data from the form
        username = form.cleaned_data['username']
        password1 = form.cleaned_data['password1']
        password2 = form.cleaned_data['password2']
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        user_type = form.cleaned_data['user_type']

        # to ensure the username is lowercase for consistency
        if not username.islower():
            return render(request, 'signup.html', {
                'form': form,
                'error': 'Username must be lowercase'
            })

        # confirm that both passwords match
        if password1 != password2:
            return render(request, 'signup.html', {
                'form': form,
                'error': 'Passwords do not match'
            })

        try:
            # Create a new user using Django's built-in User model
            user = User.objects.create_user (
                username=username,
                password=password1,
                email=email,
                first_name=name
            )

            # Assign the user to the either administrator or registrant
            #  and if the selected group does not exist it , create it in the database
            #  _ - ignores whether it was just created or already existed 
            custom_group, _ = CustomGroup.objects.get_or_create(group_name=user_type)
            # Create a record in the custom Users model linking the user to the selected group
            Users.objects.create(user=user, group=custom_group)

            # Log the user in after successful registration
            login(request, user)
            return redirect('events')

         # If username is already taken, show an error message
        except IntegrityError:
            return render(request, 'signup.html', {
                'form': form,
                'error': 'Username already taken'
            })
        
     # If form is invalid, show error
    return render(request, 'signup.html', {
        'form': form,
        'error': 'Invalid form submission'
    })


# View to handle login
def loginaccount(request):
    if request.method == 'GET':
         # Show the login form
        return render(request, 'login.html', {'form': AuthenticationForm()})
     # Handle login form submission
    form = AuthenticationForm(request, data=request.POST)
    if form.is_valid():
        # If login is successful, log the user in and redirect to events
        login(request, form.get_user())
        return redirect('events')
    else:
        # Show error if credentials are invalid
        return render(request, 'login.html', {
            'form': form,
            'error': 'Invalid login'
        })

# View to handle logout
def signoutaccount(request):
    logout(request)
    # Logs the user out and redirects to login page
    return redirect('loginaccount')
