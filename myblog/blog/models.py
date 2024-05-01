from django.db import models
from django.urls import reverse # Used in get_absolute_url() to get URL for specified ID

class Post(models.Model):
    # model representing a blog post
    id = models.BigAutoField(help_text="Post ID", primary_key=True)
    title = models.CharField(max_length=100)
    writer = models.CharField(max_length=100)
    content = models.TextField(max_length=5000)
    date = models.DateField()
    likes = models.IntegerField()

    class Meta:
        ordering = ['-date']

    def __str__(self):
        # String for representing the Model object.
        return self.title
    
    def get_absolute_url(self):
        # Returns the URL to access a detail record for this book.
        return reverse('blog-detail', args=[str(self.id)])

class Comment(models.Model):
    # model representing a comment
    id = models.BigAutoField(help_text="Comment ID", primary_key=True)
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    writer = models.CharField(max_length=100)
    content = models.CharField(max_length=200)
    date = models.DateField()
    likes = models.IntegerField()
    dislikes = models.IntegerField()

    class Meta:
        ordering = ['likes', 'dislikes']
        
    def __str__(self):
        # String for representing the Model object.
        return self.title
    
    def get_absolute_url(self):
        # Returns the URL to access a detail record for this book.
        return reverse('comment-detail', args=[str(self.id)])