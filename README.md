# django_tutorials
Django tutorial course just to cover the basics and to have something to reference at all times.



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

## I LEFT OFF AT 18:01 on Tutorial 7

https://www.youtube.com/watch?v=lHYzmlx2Vso
