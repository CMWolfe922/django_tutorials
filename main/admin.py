from django.contrib import admin
from .models import Article, ArticleSeries
# Register your models here.

class ArticleSeriesAdmin(admin.ModelAdmin):

    fields = [
        'title',
        'subtitle',
        'slug',
        # 'publish_date',
    ]


class ArticleAdmin(admin.ModelAdmin):

    fieldsets = (
        ('Header', {'fields': ['title', 'subtitle', 'article_slug', 'series']}),
        ("Content", {'fields': ['content', 'notes']}),
        ("Date", {'fields': ['modified']}),
    )

admin.site.register(ArticleSeries, ArticleSeriesAdmin)
admin.site.register(Article, ArticleAdmin)
