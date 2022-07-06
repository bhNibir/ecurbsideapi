from django.contrib import admin

from disease.models import Disease, DiseaseCategories, FavoriteDisease


# Register your models here.
@admin.register(Disease)
class DiseaseAdmin(admin.ModelAdmin):
    list_display = ("id", "disease_name", "descriptions", "create_by", "created_at", )


@admin.register(DiseaseCategories)
class DiseaseCategoriesAdmin(admin.ModelAdmin):
    list_display = ("id", "name")

@admin.register(FavoriteDisease)
class FavoriteDiseaseAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "disease", "is_favorite", "created_at", "updated_at")
