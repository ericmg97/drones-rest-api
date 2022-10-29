# Generated by Django 3.2.16 on 2022-10-29 18:26

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medication',
            name='code',
            field=models.CharField(max_length=50, primary_key=True, serialize=False, unique=True, validators=[django.core.validators.MinLengthValidator(5), django.core.validators.RegexValidator(message='Only uppercase, numbers and underscore.', regex='[A-Z0-9_]+')]),
        ),
        migrations.AlterField(
            model_name='medication',
            name='name',
            field=models.CharField(max_length=255, validators=[django.core.validators.MinLengthValidator(5), django.core.validators.RegexValidator(message='Only Alphanumeric, underscore and score.', regex='[a-zA-Z0-9_-]+')]),
        ),
    ]
