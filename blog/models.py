from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager



class Post(models.Model):

    STATS_OPTIONS = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=200)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='blog_posts', 
        )
    
    body = models.TextField()
    published_date = models.DateTimeField(default=timezone.now)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=10,
        choices=STATS_OPTIONS,
        default='draft')
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    tags = TaggableManager()

    
    class Meta:
        ordering = ('-published_date',)

    def __str__(self):
        return self.title
    
    def get_url(self):
        return reverse(
            'blog:detail',
            args=[
                self.published_date.year,
                self.published_date.month,
                self.published_date.day,
                self.slug
            ]
        )

class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    username = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.username, self.post)