from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import UserRegistrationForm, UserLoginForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm

from .decorators import user_not_authenticated

# Create your views here.
@user_not_authenticated # checks if user is authenticated or not and sends to home page if they are
def register(request):
    # Check if the request method equals POST
    if request.method == "POST":
        # create a form variable and feed it the request.POST submission
        form = UserRegistrationForm(request.POST)
        # then check if form is valid
        if form.is_valid():
            # if form is valid save it and then login to the account and get redirected to homepage
            user = form.save()
            login(request, user)
            messages.success(request, f"New account created: {user.username}")
            return redirect('/')

        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    else:
        form = UserRegistrationForm()

    return render(
        request=request,
        template_name = "users/register.html",
        context={"form": form}
        )

@login_required
def custom_logout(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("homepage")

@user_not_authenticated 
def custom_login(request):

    if request.method == "POST":
        form = UserLoginForm(request=request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            if user is not None:
                login(request, user)
                messages.success(request, f"Hello <b>{user.username}</b>! You have been logged in!")
                return redirect("homepage")
        
        else:
            for key, error in list(form.errors.items()):
                if key == 'captcha' and error[0] == 'This field is required.':
                    messages.error(request, "You must pass the reCAPTCHA test!")
                    continue

                messages.error(request, error)

    form = UserLoginForm()

    return render(
        request=request,
        template_name="users/login.html",
        context={"form": form},
    )