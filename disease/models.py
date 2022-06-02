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



class FavoriteDisease(models.Model):

    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favorite_user')
    disease = models.ForeignKey(to=Disease, on_delete=models.CASCADE, related_name='favorite_disease')
    is_favorite = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    

    class Meta:
        verbose_name_plural = "Favorite Diseases"
        constraints = [
            models.UniqueConstraint(fields=['user', 'disease'], name='favorite_once')
        ]


    def __str__(self):
        return f' {self.user}   {self.disease}  {self.is_favorite}'
