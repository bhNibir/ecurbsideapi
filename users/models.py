import datetime

from disease.models import DiseaseCategories
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/profile/<filename>
    return 'user_{0}/profile/pic/{1}'.format(instance.id, filename)

class MedicalProvider(models.Model):

    name = models.CharField(max_length=256, unique=True)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "Medical Provider Type"


class MedicalSetting(models.Model):
    
    name = models.CharField(max_length=256, unique=True)

    def __str__(self):
        return self.name


# class ProfessionalProfile(models.Model):

#     user = models.OneToOneField(CustomUser, primary_key=True, on_delete=models.CASCADE, related_name='professional_profile')
#     health_provider = models.BooleanField(default=False)
#     medical_provider_type = models.ForeignKey(to=MedicalProvider, on_delete=models.CASCADE, related_name='medical_provider', null=True)
#     medical_specialty = models.ManyToManyField(to=DiseaseCategories, related_name='medical_specialty')
#     medical_setting = models.ForeignKey(to=MedicalSetting, on_delete=models.CASCADE, related_name='medical_setting', null=True)
#     update_date = models.DateTimeField(auto_now=True)
    
#     def __str__(self):
#         return f'{self.user} - {self.user.email}'
#     class Meta:
#         verbose_name_plural = " User Professional Profile"


# @receiver(post_save, sender=CustomUser)
# def createProfile(sender, instance, created, *args, **kwargs):
#     if created:
#         ProfessionalProfile.objects.create(user=instance)
        



class CustomUser(AbstractUser):

    first_name = models.CharField(max_length=256, blank=False)
    last_name = models.CharField(max_length=256, blank=False)
    email = models.EmailField(blank=False, max_length=254, verbose_name="email address", unique=True)
    phone_number = PhoneNumberField(null = True, blank = True)
    profile_picture = models.ImageField(upload_to = user_directory_path, blank=True, null=True)
    country = CountryField(blank=True, default="US")
    health_provider = models.BooleanField(default=False)
    medical_provider_type = models.ForeignKey(to=MedicalProvider, on_delete=models.CASCADE, related_name='medical_provider', null=True)
    medical_specialty = models.ManyToManyField(to=DiseaseCategories, related_name='medical_specialty')
    medical_setting = models.ForeignKey(to=MedicalSetting, on_delete=models.CASCADE, related_name='medical_setting', null=True)
    
    USERNAME_FIELD = "username"   
    EMAIL_FIELD = "email"        

    def __str__(self):
        return self.username
    class Meta:
        verbose_name_plural = " User Personal Profile"
