from django.db import models
from django.utils import timezone

# in order to use the tinymce app in my website models, I have to import it into models
# and then change the textfields that I want to use this app to HTMLField
from tinymce.models import HTMLField

class ArticleSeries(models.Model):
    title = models.CharField(max_length=150)
    subtitle = models.CharField(max_length=255, default="", blank=True)
    series_slug = models.SlugField('Series slug', null=False, blank=False, unique=True)
    publish_date = models.DateTimeField("Date Published", default=timezone.now)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Series'
        ordering = ['-publish_date']

class Article(models.Model):
    title = models.CharField(max_length=150)
    subtitle = models.CharField(max_length=255, default="", blank=True)
    article_slug = models.SlugField('Article slug', null=False, blank=False, unique=True)
    content = HTMLField(blank=True, default="")
    # create a new field for notes then add it to the admin.py files fieldset
    notes = HTMLField(blank=True, default="")
    publish_date = models.DateTimeField("Date Published", default=timezone.now)
    modified = models.DateTimeField("Date Modified", default=timezone.now)
    series = models.ForeignKey(ArticleSeries, default='', verbose_name='Series', on_delete=models.SET_DEFAULT)

    # Create a __str__ method
    def __str__(self):
        return self.title

    # I need to create a method that creates a slug field and use property decorator
    @property
    def slug(self):
        return self.article_slug

    class Meta:
        verbose_name_plural = "Article"
        ordering = ['-publish_date']
