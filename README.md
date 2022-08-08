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






