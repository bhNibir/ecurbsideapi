from django.contrib import admin

from treatment.models import Treatment, TreatmentCategories


# Register your models here.
@admin.register(Treatment)
class TreatmentAdmin(admin.ModelAdmin):
    list_dispaly = "__all__"
   


@admin.register(TreatmentCategories)
class TreatmentCategoriesAdmin(admin.ModelAdmin):
    list_dispaly = "__all__"
   
