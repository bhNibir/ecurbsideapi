# Generated by Django 3.2.9 on 2022-03-11 04:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('treatment', '0002_treatment_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='treatment',
            old_name='user',
            new_name='create_by',
        ),
        migrations.RenameField(
            model_name='treatment',
            old_name='name',
            new_name='treatment_name',
        ),
    ]