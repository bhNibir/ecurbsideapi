from django.db import models

from review.models import Review

from django.conf import settings


class LikeReview(models.Model):
    sender = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, related_name='fk_likereview_sender_user')
    reviewID = models.ForeignKey(
        to=Review, on_delete=models.CASCADE, null=True, related_name='fk_like_review')

    class Meta:
        unique_together = ('reviewID', 'sender',)

    def __str__(self):
        return f'{self.pk}: {self.reviewID, self.sender}'
