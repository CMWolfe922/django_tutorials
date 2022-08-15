# django_tutorials
Django tutorials on all the basics of building web apps using Django. This course is just to cover the basics and to have something to reference at all times. 

- Also, if you are cloning/downloading this repository for the first time you will need to set it up. If you notice there is a `bin/` directory. Inside that directory is two scripts. One for a windows operating system and the other for ubuntu. So before running the appropriate shell script make sure you are in the `django_tutorials` root directory and then run: 

> ```sh . ./bin/setup_env.sh ``` OR ```sh . ./bin/setup_env_ubuntu.sh ```




#### Tutorial-6:
---


> Styling the website and getting model objects to show up.

1. Add a `templates` directory and `static` directory to the main app. Inside the `templates` directory, create the base and navbar.
- 1.1) Then inside the `static` directory add `images` and `main` directory. `main` will be where I store the `css` and `javascript` files for this app.

2. Install `fontawesomefree` then add it to the settings file in the `INSTALLED_APPS` section `fontawesomefree`

3. Inside of the `static/main` directory, create a `main.css` file where all of the websites main styling will be handled.

4. Created the home.html file:

```html
{% extends 'main/base.html' %}
{% block content %}
<div class="row display-flex justify-content-center">
    {% for object in objects %}
    <div class="col-lg-4 col-md-6 col-sm-12 mobiledevices">
        <article class="media content-section customhover" style="height: 95%;">
            <div class="media-body">
                <a href="/{{object.slug}}">
                    <img class="img-fluid" src="/" alt="">
                </a>
                <div>
                    <a class="article-title line-clamp-2 title-style" style="font-size:22px" href="/{{object.slug}}">
                        {{ object.title }}
                    </a>
                    <a href="/{{object.slug}}" style="text-decoration: none;">
                        <p class="article-content line-clamp-5 subtitle-style">{{ object.subtitle }}</p>
                    </a>
                </div>
            </div>
        </article>
    </div>
    {% endfor %}
</div>

{% endblock %}
```
5. Now in order to get this template to work. I have to create a view in the `main` apps `views.py` file. Since I already have a homepage view created I just have to import the model `ArticleSeries` and then create a variable inside the `homepage` `view` `function` called `matching_series` and then return `render(request, 'template.html', context={'objects': matching_series})`

6. Now I need to create a series view: To do this I will have to use the filter option to filter all the slugs in a series:

```python
def series(request, series: str):
    series_articles = Article.objects.filter(series__series_slug=series).all()
    return render(request, 'main/home.html', context={'objects': series_articles})

```
7. Now Comes the part where I create the `article.html` file:

```html
{% extends 'main/base.html' %}
{% block content %}
<div class="row media content-section mobiledevice">
    <div class="col-lg-12 col-md-12 col-sm-12 mt-3 mb-2">
        <div class="d-flex">
            <div>
                <h1 class="title-style">{{ object.title }}</h1>
                <h2 class="subtitle-style">{{ object.subtitle }}</h2>
            </div>
        </div>
    </div>
    <div class="col-lg-9 col-md-12 col-sm-12 mt-3 mb-2" id="content">
        <div class="article-style">
            <!-- safe means we want to render HTML code instead of text -->
            {{ object.content|safe }}
        </div>
    </div>
</div>
{% endblock %}

```

8. Now that we have a template to render our articles in, I need to add the article file to the `urlpatterns` in `urls.py`

```python
urlpatterns = [
     # 2) Django then looks here and sees to look for views.homepage view
    path('', views.homepage, name='homepage'),
    # now create a new url patter with a path to the series
    path('<series>', views.series, name='series'),
    # Add the path for rendering the articles: This means I have to create a articles view
    path('<series>/<article>', views.article, name='article'),
]
```

9. From here I will create a new view for `articles.html`: First I need to go to the `models.py` file where I created the `slug` method with a `@property` decorator and join `series_slug` with `article_slug`

###### main/models.py
```python
...

    # I need to create a method that creates a slug field and use property decorator
    @property
    def slug(self):
        return self.series.series_slug + '/' + self.article_slug

```

- Then whats left is the article view:

```python
# First I need to go to the models.py file where I created the slug method
# with a @property decorator and join series_slug with article_slug

def article(request, series: str, article: str):
    matching_article = Article.objects.filter(series__series_slug=series, article_slug=article).first() # instead of all get first instance
    return render(request, 'main/article.html', context={'object': matching_article})
```


---




# TUTORIAL-7: Creating User Registration
---


1. Build an html file called `registration.html` in the `template` directory of the `users` app directory

```html
<!-- First I want to extend the base.html file from main app -->
{% extends 'main/base.html' %}
{% block content %}
<div>
    <form method="POST">
        <!-- when creating a form dont forget the csrf_token -->
        {% csrf_token %}
        <fieldset class="form-group">
            <legend class="border-bottom mb-4">Join Today</legend>
        </fieldset>

        By registering, you accept the Terms of Service and Privacy Notice

        <div class="form-group">
            <button class="btn btn-outline-info" type="submit">Sign Up</button>
        </div>
    </form>
    <div class="border-top pt-3">
        <small class="text-muted">
            Already have an account? <a class="ml-2" href="/login">Sign In</a>
        </small>
    </div>
</div>
{% endblock %}

```

2. Next I will have to create a form to create new user accounts:

```python
from django.forms import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model



class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(help_text="A valid email address required")

    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()

        return user

```

3. Now that the form is ready, I will have to create the view in views.py

```python
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login
from .forms import UserRegistrationForm


# Create your views here.
def register(request):

    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        # check if form is valid
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')

        else:
            for error in list(form.errors.values()):
                print(request, error)

    else:
        form = UserRegistrationForm()

    return render(request, 'registeration.html', {'form': form})

```


===

---

# TUTORIAL 8: Messaging
---


> In the `users` app move the `register.html` to another folder in the `templates` directory to the `users` directory inside `templates` directory.

- Then go to `views.py` in the `users` app and at the end of the register function change the template_name to include:
    - `template_name = 'users/register.html'`


---

#### NOW LETS MOVE TO THE DJANGO MESSAGING TUTORIAL:

We can display messages to users using the django messaging framework. I can also control how they are displayed and who sees them. 

One use case would be to notify the user (after they register) that they have successfully registered, or that they need to fix something to register. This can also be used for any task in the app that requires the user to submit a form or perform a task. 
    - adding contacts
    - messaging someone else - success message
    - logging in and out - message confirming either
    - receiving a message - popout notifictation
    - receiveing a like or sometype of request from another user


> So to start I will go to the `views.py` file in the `users` app and then begin adding messages their:

- So to do this I will have to import the messages packages `from django.contrib import messages` . Then after the `login(request, user)` line, I will add the messages function/method to create a message upon successfully logging in: 

```python
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login
# ===== NEW IMPORT TO THIS FILE ====== #
from django.contrib import messages
# ==================================== #
from django.contrib.auth.decorators import wraps, resolve_url
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
```

- The best place to create a template to handle a message template is after our navbar since every file will have the navbar.

So inside the `main` app, go to the `templates/includes/` directory and add a `messaging.html` file. This will be the same directory that has the `navbar.html` file inside of it. 

> This is the `messaging.html` template

- `messaging.html`
```html

<!-- CREATE MAIN IF STATEMENT TO DETERMINE WHICH MESSAGE IS DISPLAYED -->
{% if messages %}
    <!-- NOW ITERATE THROUGH THE MESSAGES -->
    {% for message in messages %}
        <!-- This is where the message type checks begin starting with 'success messages' -->
        {% if message.tags == 'success' %}
        <div class="alert alert-success alert-dismissible" role="alert">
            <a href="#" class="close" data-dismiss="alert" aria-label="close">&times;</a>
            {{ message|safe|escape }}
        </div>
        {% elif message.tags == 'error' %}
        <div class="alert alert-danger alert-dismissible" role="alert">
            <a href="#" class="close" data-dismiss="alert" aria-label="close">&times;</a>
            {{ message|safe }}
        </div>
        {% elif message.tags == 'info' %}
        <div class="alert alert-info alert-dismissible" role="alert">
            <a href="#" class="close" data-dismiss="alert" aria-label="close">&times;</a>
            {{ message|safe|escape }}
        </div>
        {% elif message.tags == 'warning' %}
        <div class="alert alert-warning alert-dismissible" role="alert">
            <a href="#" class="close" data-dismiss="alert" aria-label="close">&times;</a>
            {{ message|safe|escape }}
        </div>
        {% endif %}
        <!-- End the first if and the only for statement -->
    {% endfor %}
    <!-- Final endif statement -->
{% endif %}
```

### Now that the messaging template is created: 
---

> I have to go the `base.html` file and then add the `messaging.html` template to an include statement after the row and column sections:

`base.html` setup from before: 

```html
{% load static %}
<!doctype html>
<html lang="en">

<head>
    {% block head %}
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <!-- Bootstrap4.6 CSS -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.1/dist/css/bootstrap.min.css"
        integrity="sha384-zCbKRCUGaJDkqS1kPbPd7TveP5iyJE0EjAuZQTgFLD2ylzuqKfdKlfG/eSrtxUkn" crossorigin="anonymous">

    <!-- Add Bootstrap icons CDN Under here -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.9.0/font/bootstrap-icons.css">

    <!-- Add FontAwesome CDN -->
    <script src="https://kit.fontawesome.com/216d1cce07.js" crossorigin="anonymous"></script>

    <!-- Add Custom CSS file -->
    <link rel="stylesheet" type="text/css" href="{% static 'main/main.css' %}">

    <!-- Jquery JS -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>

    {% endblock %}
    <title>{% block title %}App Title: Base{% endblock %}</title>
</head>

<body>

    {% include 'main/includes/navbar.html' %}
    <div class="container-fluid">
        {% block content %}
        {% endblock %}
    </div>



    <!-- jQuery and Bootstrap Bundle (includes Popper) -->
    <script src="https://cdn.jsdelivr.net/npm/jquery@3.5.1/dist/jquery.slim.min.js"
        integrity="sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj"
        crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.6.1/dist/js/bootstrap.bundle.min.js"
        integrity="sha384-fQybjgWLrvvRgtW6bFlB7jaZrFsaBXjsOMm/tB9LTS58ONXgqbR9W8oWht/amnpF"
        crossorigin="anonymous"></script>

    <!-- Optional JavaScript: This points to the custom.js file in main apps static/main directory -->
    <script type="text/javascript" src="https://{% static 'main/custom.js' %}"></script>
</body>

</html>

```

This is the new setup for the `base.html` file:

```html
{% load static %}
<!doctype html>
<html lang="en">

<head>
    {% block head %}
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <!-- Bootstrap4.6 CSS -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.1/dist/css/bootstrap.min.css"
        integrity="sha384-zCbKRCUGaJDkqS1kPbPd7TveP5iyJE0EjAuZQTgFLD2ylzuqKfdKlfG/eSrtxUkn" crossorigin="anonymous">

    <!-- Add Bootstrap icons CDN Under here -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.9.0/font/bootstrap-icons.css">

    <!-- Add FontAwesome CDN -->
    <script src="https://kit.fontawesome.com/216d1cce07.js" crossorigin="anonymous"></script>

    <!-- Add Custom CSS file -->
    <link rel="stylesheet" type="text/css" href="{% static 'main/main.css' %}">

    <!-- Jquery JS -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>

    {% endblock %}
    <title>{% block title %}App Title: Base{% endblock %}</title>
</head>

<body>
    {% include 'main/includes/navbar.html' %}
    <main role="main" class="container-xl">
        <div class="row">
            <div class="col-lg-12 col-md-12-p-0 col-sm-12">
                {% include 'main/includes/messaging.html' %}
                {% block content %}
                {% endblock %}
            </div>
        </div>
    </main>

    <!-- jQuery and Bootstrap Bundle (includes Popper) -->
    <script src="https://cdn.jsdelivr.net/npm/jquery@3.5.1/dist/jquery.slim.min.js"
        integrity="sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj"
        crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.6.1/dist/js/bootstrap.bundle.min.js"
        integrity="sha384-fQybjgWLrvvRgtW6bFlB7jaZrFsaBXjsOMm/tB9LTS58ONXgqbR9W8oWht/amnpF"
        crossorigin="anonymous"></script>

    <!-- Optional JavaScript: This points to the custom.js file in main apps static/main directory -->
    <script type="text/javascript" src="https://{% static 'main/custom.js' %}"></script>
</body>

</html>
```

- Now if I fillout the registration form with wrong information, I should receive a message stating what I did wrong...

- The messages worked. They were displayed at the top letting me know when an error or some other information occured. 


===


# TUTORIAL 9: Login and Logout:
---


To startout I will focus on the `navbar.html` because here I can change which icons show up regarding the login or logout icons. I can run an if statement check to see if the user is logged in or not. To do this I will use the classic `{% if user.is_authenticated %}`

- A simple way to get started adding this into a file is by going close to where you want to implement this inside the file and just create the if, else and endif django tags so that you can easily insert the proper code where it goes: 

```html
...

{% if user.is_authenticated %}
{% else %}
{% endif %}

...

```

> Now lets take the navbar and then begin to implement this. first, I must create a new branch for tutorial 9: This will be the Login and Logout tutorial. I will also learn about verifiying user access and whether the user is logged in and has access to the data they request:

Now I need to copy and paste the `navbar.html` file into this README file so that I can make the required changes:

```html
<header class="site-header" style="margin-bottom: 5px;">
    <nav class="navbar navbar-expand-md navbar-color">
        <div class="container">
            <div class="navbar-nav">
                <a class="nav-item nav-link" href="/">Home</a>
            </div>
            <button aria-controls="navbarToggle" aria-expanded="false" aria-label="Toggle navigation" class="navbar-toggler ml-auto float-right btncolor" data-target="#navbarToggle" data-toggle="collapse" type="text">
                <i class="fas fa-bars fa-2x"></i>
            </button>
            <div class="collapse navbar-collapse" id="navbarToggle">
                <!-- navbar left side -->
                <div class="navbar-nav mr-auto">
                    <a class="nav-item nav-link" href="/">About</a>
                </div>
                <!-- navbar Right Side -->
                <!-- Where the user verification starts -->
                <div class="navbar-nav">
                    {% if user.is_authenticated %}
                        <a class="nav-item nav-link" href="{% url 'logout' %}">
                            Log Out <i class="fas fa-sign-out-alt"></i>
                        </a>
                    {% else %}
                        <a class="nav-item nav-link" href="{% url 'login' %}">
                            Login <i class="fas fa-sign-in-alt"></i>
                        </a>
                        <a class="nav-item nav-link" href="{% url 'register' %}">
                            Sign Up <i class="fas fa-user-plus"></i>
                        </a>
                    {% endif %}
                </div>
            </div>
        </div>
    </nav>
</header>
```

> When the above template was created in the README file, there was no such thing as the login or logout templates. So it would've created an error. Therefore, before adding this to the project file. I can now go and create the required templates. ALSO, I need to create the `urlpatterns`. On this topic, I will show what to do below:

`users/urls.py`
```python
from django.urls import path
from . import views
# ============================================================================================ #
# THIS WAS IMPORTED FOR THE BELOW URLPATTERNS
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("register/", views.register, name="register"),
    # ============================================================================================ #
    # THESE ARE THE ADDED URLS: 
    # ============================================================================================ #
    # Now create my new login and logout paths:
    path('login', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
]
```

- First I created the `login.html` file so that users can freely login and logout:
###### `login.html`
```html 
{% extends "main/base.html" %}
{% load crispy_forms_tags %}
{% block content %}
<div>
    <form method="POST">
        {% csrf_token %}
        <fieldset class="form-group">
            <legend class="border-bottom mb-4">Log In</legend>
            {{ form|crispy }}
        </fieldset>
        <div class="form-group">
            <button class="btn btn-outline-info" type="submit">Login</button>
        </div>
    </form>
    <div class="border-top pt-3">
        <small class="text-muted">
            Need An Account? <a class="ml-2" href="{% url 'register' %}">Sign Up Now</a>
        </small><br>
        <small class="text-muted">
            <a href="/">Forgot Password?</a>
        </small>
    </div>
</div>
{% endblock %}
```

- The next file created was the logout file. 
###### `logout.html`
```html
{% extends "main/base.html" %}
{% block content %}
<div class="justify-content-center">
    <h2> You have been successfully logged out! </h2>
    <div class="border-top pt-3" style="min-height:65vh;">
        <small class="text-muted">
            <a href="{% url 'login' %}">Log In Again</a>
        </small>
    </div>
</div>
{% endblock %}
```

> Now that I have the basic files created I can update the navbar.html file to include the logic and user authentication to determine what to show: 



# TUTORIAL 10: Django Decorators and Email Login
---


> This tutorial will be about learning to use Django decorators. Decorators can be used to require login, catching errors, and many other tasks.

- Decorators can accept arguments and are used to change the behavior of functions. 

To get started, I will create a new script file `decorators.py` in the `users` app. I will copy and paste the code below and then describe what the code does. 

`users/decorators.py`
```python
from django.shortcuts import redirect


# Create a basic function for user not authenticated
def user_not_authenticated(function=None, redirect_url='/'):
    """
    :description: The main purpose of this decorator function is check if the user 
    is authenticated or not. If the user is authenticated then we need to redirect
    the user back to specified url. (USuaully Homepage) 

    :param functions: 

    :param redirect_url:
    """

    # Now create another function inside this function called decorator
    def decorator(view_func):
        # and then one more function called _wrapped_view
        def _wrapped_view(request, *args, **kwargs):
            # This will return the user to the homepage if the user is authenticated
            if request.user.is_authenticated:
                return redirect(redirect_url)

            # but if the above check doesn't work, we still need to return something. 
            # in this case it will be the view function
            return  view_func(request, *args, **kwargs)

        return _wrapped_view

    if function: # is not None
        # then return the decorator function that you want to use
        return decorator(function)

    return decorator
```

- This decorator function allows me to remove some code out of the view functions. Below shows what code it replaces:

`users/views.py`
```python
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login, logout, authenticate
from django.contrib import messages
from .forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm

from .decorators import user_not_authenticated

# Create your views here.
@user_not_authenticated
def register(request):
    # BELOW CODE IS REPLACED BY THE DECORATOR FUNCTION
    # ============================================================================== #
    # # Check if the user is logged in already or not:
    # if request.user.is_authenticated:
    #     # if user is already logged in, send them to homepage
    #     return redirect('/')
    # ============================================================================== #
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
    # BELOW CODE IS REPLACED BY THE DECORATOR FUNCTION
    # ============================================================================== #
    # if request.user.is_authenticated:
    #     return redirect("homepage")
    # ============================================================================== #

    if request.method == "POST":
        form = AuthenticationForm(request=request, data=request.POST)
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
            for error in list(form.errors.values()):
                messages.error(request, error)

    form = AuthenticationForm()

    return render(
        request=request,
        template_name="users/login.html",
        context={"form": form},
    )
```


#### Tutorial 10: Email Login Form

> Now I will create a custom email login form. This will basically be a custom authentication system by creating some work around hacks. 

So in the `users/forms.py` file I will create a new form object that I will add to the registration and login process. 

`users/forms.py`
```python 
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm # <---- ADDED THE AuthenticationForm import as well
from django.contrib.auth import get_user_model


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(help_text='A valid email address, please.', required=True)

    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()

        return user

# ======================================================================================== #
# ADDED THIS NEW USER LOGIN FORM OBJECT
# ======================================================================================== #
class UserLoginForm(AuthenticationForm):

    def __init__(self,*args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Username of Email'}),
            label="Username or Email")

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Password'}))
```

In order to use the new `UserLoginForm`, I will have to import this to the `users/view.py` file and then replace the `AuthenticationForm` objects with the new `UserLoginForm` object

Now that we have the `UserLoginForm` created and working, I need to now create an authentication for the backend. This way the login process and emails can be authenticated properly using a custom authentication process. 

To start off, create a new script file in the `users` app called `backends.py`

`users/backends.py`
```python
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

UserModel = get_user_model()
class EmailBackend(ModelBackend):
    """
    Authenticates against settings.AUTH_USER_MODEL.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        try: 
            # This basically queries the database in search of a match for the username or email
            user = UserModel.objects.get(Q(username__iexact=username) | Q(email__iexact=username))

        # Now I need to create an exception incase there is no such username or email in the database:
        except UserModel.DoesNotExist:
            UserModel().set_password(password)
            return

        except UserModel.MultipleObjectsReturned:
            user = UserModel.objects.get(Q(username__iexact=username) | Q(email__iexact=username)).order_by('id').first()

        if user.check_password(password) and self.user_can_authenticate(user):
            return user

```

- Now that the `EmailBackend` object is built, I need to go to the `settings.py` file and modify some of the settings so that I can implement my new backend. 

in `settings.py` add the following changes:

`django_site/settings.py`
```python
# Adding the backend authentication setting that I created for the EmailBackend object
AUTHENTICATION_BACKENDS = ['users.backends.EmailBackend']
```

- That should override the django authentication settings


---

# TUTORIAL 11: Implementing Google reCAPTCHA security
---


The first thing you have to do to implement reCAPTCHA is go to the [google reCAPTCHA website](https://www.google.com/recaptcha/about/) create an account (or if you already have an account, create a new website instance to use). 

Next, I need to install the third party django package, __django-recaptcha__, using `pip`: 
    `pip install django-recaptcha`

> Once the pip package is installed, I need to go to settings and add the `captcha` package to `INSTALLED_APPS`

Now I will add the captcha field to my form in the `users/forms.py` file:
 
```python
...
# THIS NEED TO BE IMPORTED TO THE SCRIPT
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
...


class UserLoginForm(AuthenticationForm):

    def __init__(self,*args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Username of Email'}),
            label="Username or Email")

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Password'}))

    # ================================================================================= #
    # THIS IS WHAT WAS ADDED FOR THE reCAPTCHA FIELD
    # ================================================================================= #
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox(attrs={'data-theme': 'dark'}))
```

- In the settings file I added the public and private keys as well as a setting that is used for the development version of the website. Once the website/app is launched, then this setting will be removed. 

`django_site/settings.py`
```python
# ADDING THE RECAPTCHA SETTINGS:
RECAPTCHA_PUBLIC_KEY = '6Lc09nchAAAAAPzFjaRfenIGDOYgHr3X1uqgzBKX'
RECAPTCHA_PRIVATE_KEY = '6Lc09nchAAAAAF9qc3Rx0sXOgrbni9eU4XEHNRFr'
# I have to add this to the development version
SILENCED_SYSTEM_CHECKS = ['captcha.recaptcha_test_key_error']
```

Now, I need to change the message that is displayed if the user fails to use the captcha checkbox when signing in. I can use my debug script to see where and how to change the message that is displayed by default with the reCAPTCHA 