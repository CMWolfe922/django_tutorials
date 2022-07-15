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
