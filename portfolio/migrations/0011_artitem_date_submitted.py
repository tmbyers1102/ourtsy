# Generated by Django 3.1.4 on 2021-08-17 16:54

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0010_auto_20210817_1635'),
    ]

    operations = [
        migrations.AddField(
            model_name='artitem',
            name='date_submitted',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
