# Generated by Django 3.1.4 on 2021-09-14 21:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('portfolio', '0004_auto_20210914_0949'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='approval_status',
            field=models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='portfolio.approvalstatus'),
        ),
        migrations.AddField(
            model_name='post',
            name='publish_after_approved',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='post',
            name='review_note',
            field=models.TextField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='reviewed_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='post_reviewer', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='post',
            name='status',
            field=models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='portfolio.artstatus'),
        ),
        migrations.AddField(
            model_name='post',
            name='urgent_review',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='post',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_author', to=settings.AUTH_USER_MODEL),
        ),
    ]
