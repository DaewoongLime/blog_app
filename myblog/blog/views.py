from django.shortcuts import render
from django.views import generic
from .models import Post, Comment

# Create your views here.
# def home(request):
#     posts = Post.objects.all()

#     context = {
#         'posts':posts,
#         'num_posts':posts.count()
#     }

#     return render(request, 'home.html', context=context)

class PostListView(generic.ListView):
    model = Post
    context_object_name = 'posts'   # your own name for the list as a template variable
    # queryset = Post.objects.filter(title__icontains='war')[:5] # Get 5 books containing the title war
    template_name = 'home.html'  # Specify your own template name/location
    paginate_by = 10
    # ?page=2

class PostDetailView(generic.DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'post.html'
