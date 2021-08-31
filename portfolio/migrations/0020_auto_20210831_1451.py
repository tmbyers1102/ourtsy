# Generated by Django 3.1.4 on 2021-08-31 21:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0019_auto_20210823_0950'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artimage',
            name='art_item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='has_images', to='portfolio.artitem'),
        ),
        migrations.AlterField(
            model_name='artitem',
            name='artist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='art_items', to='portfolio.artist'),
        ),
    ]
