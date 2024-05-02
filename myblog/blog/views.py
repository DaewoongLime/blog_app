from django.shortcuts import render
from .models import Post, Comment

# Create your views here.
def home(request):
    posts = Post.objects.all()

    context = {
        'posts':posts,
        'num_posts':posts.count()
    }

    return render(request, 'home.html', context=context)
