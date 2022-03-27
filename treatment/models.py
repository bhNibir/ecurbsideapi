from datetime import datetime

from disease.models import Disease
from django.conf import settings
from django.db import models


class TreatmentCategories(models.Model):
    
    name = models.CharField(max_length=100, unique=True)
    class Meta:
        verbose_name_plural = "Treatment Categories"

    def __str__(self):
        return self.name



def user_directory_path(instance, filename):
    _now = datetime.now()
    # file will be uploaded to MEDIA_ROOT/user_<id>/uploads/2021/Jan/01/<filename>
    return 'user_{id}/uploads/{year}/{month}/{day}/{filename}'.format(id= instance.create_by.id,
                                 year=_now.strftime('%Y'),
                                 month=_now.strftime('%b'), 
                                 day=_now.strftime('%d'), 
                                 filename=filename)

class Treatment(models.Model):

    disease = models.ForeignKey(to=Disease, related_name='treatment_disease', on_delete=models.CASCADE)
    
    treatment_name = models.CharField(max_length=200)

    other_name = models.CharField(max_length=200, blank=True, null=True)

    treatment_categories = models.ForeignKey(to=TreatmentCategories, related_name='fk_treatment_category', on_delete=models.SET_NULL, null=True)

    image = models.ImageField(upload_to=user_directory_path, blank=True, null=True)
    
    descriptions = models.TextField()    

    create_by = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='fk_treatment_user')

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    
    class Meta:
            constraints = [
                models.UniqueConstraint(
                    fields=['disease', 'treatment_name', 'treatment_categories'], 
                    name='unique treatment name'
                )
            ]

    def __str__(self):
        return self.treatment_name


    