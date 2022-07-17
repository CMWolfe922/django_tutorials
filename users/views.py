from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import wraps, resolve_url
from django.contrib import messages
from .forms import UserRegistrationForm


# Create your views here.
def register(request):
    # Check if the user is logged in already or not:
    if request.user.is_authenticated:
        # if user is already logged in, send them to homepage
        return redirect('/')
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