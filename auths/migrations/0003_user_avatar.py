# Generated by Django 3.1.2 on 2020-10-26 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auths', '0002_user_is_staff'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='avatars/'),
        ),
    ]
