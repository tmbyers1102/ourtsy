# Generated by Django 3.1.4 on 2021-09-15 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0007_auto_20210914_1428'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=models.SlugField(blank=True, editable=False, max_length=100, primary_key=True, serialize=False, unique=True),
        ),
    ]
