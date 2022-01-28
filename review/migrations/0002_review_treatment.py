# Generated by Django 3.2.9 on 2022-01-28 14:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('treatment', '0001_initial'),
        ('review', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='treatment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fk_review_treatment', to='treatment.treatment'),
        ),
    ]
