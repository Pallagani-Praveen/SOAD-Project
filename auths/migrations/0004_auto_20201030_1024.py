# Generated by Django 3.1 on 2020-10-30 04:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auths', '0003_user_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='gender',
            field=models.CharField(choices=[('male', 'MALE'), ('female', 'FEMALE')], default='male', max_length=6),
        ),
        migrations.AddField(
            model_name='user',
            name='is_dealer',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='is_farmer',
            field=models.BooleanField(default=False),
        ),
    ]
