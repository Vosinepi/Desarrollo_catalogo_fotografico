# Generated by Django 4.1.2 on 2022-10-10 16:38

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('catalogo_fotos_app', '0003_album_es_publico'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='users_permitions',
            field=models.ManyToManyField(default='admin', related_name='users_permitions', to=settings.AUTH_USER_MODEL),
        ),
    ]
