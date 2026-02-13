from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Post(models.Model):
    """
    Blog post model
    """
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    
    class Meta:
        ordering = ['-published_date']  # Most recent posts first
        
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})