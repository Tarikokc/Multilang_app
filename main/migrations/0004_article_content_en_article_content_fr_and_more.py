# Generated by Django 5.0.6 on 2024-06-17 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_alter_article_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='content_en',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='article',
            name='content_fr',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='article',
            name='title_en',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='article',
            name='title_fr',
            field=models.CharField(max_length=300, null=True),
        ),
    ]
