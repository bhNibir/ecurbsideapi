from django.conf import settings
from django.db import models

from review.models import Review


class Comment(models.Model):

    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, related_name='fk_comment_user')

    review = models.ForeignKey(to=Review, on_delete=models.CASCADE, null=True, related_name='fk_comment_review')

    content = models.CharField(max_length=400)

    created = models.DateTimeField(auto_now_add=True)

    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user} - {self.review}'
