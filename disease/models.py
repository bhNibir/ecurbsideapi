from pickle import TRUE
from django.conf import settings
from django.db import models


class DiseaseCategories(models.Model):
    
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "Disease Categories"

    def __str__(self):
        return self.name


class Disease(models.Model):
    
    disease_name = models.CharField(max_length=200, unique=TRUE)

    disease_categories = models.ManyToManyField(to=DiseaseCategories, related_name='diseases_categories')
    
    descriptions = models.TextField()    

    create_by = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='disease_user')

    created_at = models.DateTimeField(auto_now_add=True)
    
    updated_at = models.DateTimeField(auto_now=True)    


    def __str__(self):
        return self.disease_name
