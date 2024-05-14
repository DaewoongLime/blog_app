from django.contrib.auth.models import User
from django.db import models
from django.db.models import Count, Q
from django.urls import reverse # Used in get_absolute_url() to get URL for specified ID
from datetime import datetime    

class Post(models.Model):
    # model representing a blog post
    id = models.BigAutoField(help_text="Post ID", primary_key=True)
    title = models.CharField(max_length=100)
    writer = models.CharField(max_length=100)
    content = models.TextField(max_length=5000)
    date = models.DateTimeField(default=datetime.now, blank=True)
    likes = models.IntegerField(default=0)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('post', args=[str(self.id)])

class Comment(models.Model):
    # model representing a comment
    id = models.BigAutoField(help_text="Comment ID", primary_key=True)
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    writer = models.CharField(max_length=100)
    content = models.CharField(max_length=200)
    date = models.DateTimeField(default=datetime.now, blank=True)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)

    class Meta:
        ordering = ['-date']
        
    def __str__(self):
        # String for representing the Model object.
        return str(self.post)+" "+self.writer

class PostLike(models.Model):
    # model representing post likes
    id = models.BigAutoField(help_text="Post Like ID", primary_key=True)
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    like = models.BooleanField(default=True)

class CommentLike(models.Model):
    # model representing comment likes
    id = models.BigAutoField(help_text="Comment Like ID", primary_key=True)
    comment = models.ForeignKey("Comment", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    like = models.IntegerField()
