# Generated by Django 3.2.9 on 2022-01-28 14:34

from django.db import migrations, models
import django.db.models.deletion
import treatment.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('disease', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TreatmentCategories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
            options={
                'verbose_name_plural': 'Treatment Categories',
            },
        ),
        migrations.CreateModel(
            name='Treatment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('other_name', models.CharField(blank=True, max_length=200, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to=treatment.models.user_directory_path)),
                ('descriptions', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('disease', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='treatment_disease', to='disease.disease')),
                ('treatment_categories', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='fk_treatment_category', to='treatment.treatmentcategories')),
            ],
        ),
    ]
