from django.db import models
from django.utils import timezone 
from django.contrib.auth import get_user_model
from django.urls import reverse
from taggit.managers import TaggableManager


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
    tags = TaggableManager()
    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]

    def __str__(self):
        return self.title 
    
    def get_absolute_url(self):
        return reverse(
            'blog:post_detail',
            args=[
                self.publish.year,
                self.publish.month,
                self.publish.day,
                self.slug
            ]
        )


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        related_name='comments',
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta: 
        ordering = ['-created']
        indexes = [
            models.index(fiels=['created']),

        ]

    def __str__(self):
        return f'Comment by {self.name} on {self.post} sSse efsfsee'