# Generated by Django 4.2.5 on 2023-09-13 13:40

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapi', '0009_authuser_lead_alter_document_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='authuser',
            name='lead',
        ),
        migrations.AddField(
            model_name='authuser',
            name='leads',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
