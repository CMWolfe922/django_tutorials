# Generated by Django 4.0.6 on 2022-07-15 06:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_article_notes_alter_article_content'),
    ]

    operations = [
        migrations.RenameField(
            model_name='articleseries',
            old_name='series_slug',
            new_name='slug',
        ),
    ]
