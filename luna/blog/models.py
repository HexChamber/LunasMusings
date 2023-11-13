from django.db import models
from django.utils import timezone 
from django.contrib.auth import get_user_model


User = get_user_model()

# Create your models here.

class DraftsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(
            status=Post.Status.DRAFT
        )
    

class ReviewsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(
            status=Post.Status.REVIEW
        )
    

class ApprovedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(
            status=Post.Status.APPROVED
        )
    

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(
            status=Post.Status.PUBLISHED
        )
    




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
    objects = models.Manager()
    drafts = DraftsManager()
    under_review = ReviewsManager()
    approved = ApprovedManager()
    published = PublishedManager()
    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]

    def __str__(self):
        return self.title 