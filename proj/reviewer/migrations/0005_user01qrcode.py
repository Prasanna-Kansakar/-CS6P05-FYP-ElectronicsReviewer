# Generated by Django 3.2.12 on 2022-04-18 19:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reviewer', '0004_auto_20220418_1928'),
    ]

    operations = [
        migrations.CreateModel(
            name='User01QRcode',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('grant_verfication', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
