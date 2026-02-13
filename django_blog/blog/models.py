from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

from PIL import Image




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
    
    class Profile(models.Model):
    
     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', default='default.jpg', blank=True)
    website = models.URLField(max_length=200, blank=True)
    location = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return f'{self.user.username} Profile'
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        # Resize large profile images
        if self.profile_pic and hasattr(self.profile_pic, 'path'):
            try:
                img = Image.open(self.profile_pic.path)
                if img.height > 300 or img.width > 300:
                    output_size = (300, 300)
                    img.thumbnail(output_size)
                    img.save(self.profile_pic.path)
            except:
                pass  # Handle cases where image file might not exist yet