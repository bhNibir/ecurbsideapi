from django.conf import settings
from django.db import models

from treatment.models import Treatment


class Review(models.Model):
    RATING = [
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5)
    ]

    content = models.CharField(max_length=500)

    rating = models.IntegerField(choices=RATING)
    
    create_by = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name='fk_review_user')    
    
    treatment = models.ForeignKey(
        to=Treatment, on_delete=models.CASCADE, related_name='fk_review_treatment')
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.pk}: {self.create_by} - {self.treatment}'



class ReviewComment(models.Model):

    create_by = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='fk_comment_user')
    
    review = models.ForeignKey(to=Review, on_delete=models.CASCADE, related_name='fk_comment_review')
    
    content = models.CharField(max_length=400)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.create_by} - {self.review}'



class ReviewLike(models.Model):
    sender = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, related_name='fk_like_review_user')
    
    reviewID = models.ForeignKey(
        to=Review, on_delete=models.CASCADE, null=True, related_name='fk_like_review')

    class Meta:
        unique_together = ('reviewID', 'sender',)

    def __str__(self):
        return f'{self.pk}: {self.reviewID, self.sender}'