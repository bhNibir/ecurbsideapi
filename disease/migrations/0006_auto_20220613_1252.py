# Generated by Django 3.2.9 on 2022-06-13 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('disease', '0005_disease_unique disease name'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='disease',
            name='unique disease name',
        ),
        migrations.AddConstraint(
            model_name='disease',
            constraint=models.UniqueConstraint(fields=('disease_name', 'disease_categories'), name='unique disease name'),
        ),
    ]
