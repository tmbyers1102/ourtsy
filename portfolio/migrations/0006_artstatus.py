# Generated by Django 3.1.4 on 2021-08-16 22:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0005_auto_20210816_1801'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArtStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField()),
            ],
        ),
    ]
