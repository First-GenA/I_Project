# Generated by Django 5.1.5 on 2025-02-07 12:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personal', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactions',
            name='t_owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='personal.userinfo'),
        ),
    ]
