from django.db import models
from django.utils import timezone 
from django.contrib.auth import get_user_model


User = get_user_model()

# Create your models here.


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = "DF", "Draft"
        REJECT = "RJ", "Rejected"
        REVIEW = 'RW', 'Under review'
        APPROVED = "AP", "Approved"
        PUBLISHED = 'PB', 'Published'
        
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    author = models.ForeignKey(
        User,
        related_name='blog_posts',
        on_delete=models.CASCADE
    )
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.DRAFT
    )

    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]

    def __str__(self):
        return self.title 