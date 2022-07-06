from django.contrib import admin
from .models import Review, ReviewComment, ReviewLike

admin.site.register(Review)
admin.site.register(ReviewLike)
admin.site.register(ReviewComment)

# @admin.register(ReviewComment)
# class ReviewCommentAdmin(admin.ModelAdmin):
#     list_display = ("create_by", "review", "content", "created_at", "updated_at")