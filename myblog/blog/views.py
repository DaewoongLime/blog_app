from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from .models import *
from .forms import *

class PostListView(generic.ListView):
    model = Post
    context_object_name = 'posts'   # your own name for the list as a template variable
    # queryset = Post.objects.filter(title__icontains='war')[:5] # Get 5 books containing the title war
    template_name = 'home.html'  # Specify your own template name/location
    paginate_by = 5

class PostDetailView(generic.DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'view_post.html'

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        id = int(self.kwargs.get('pk'))
        comments = Comment.objects.filter(post=id).order_by('-likes', 'dislikes')[:5]
        context['comments'] = comments
        return context

class CommentListView(generic.ListView):
    model = Comment
    context_object_name = 'comments'

    def get_queryset(self):
        return Comment.objects.filter(post=self.kwargs['pk'])

    template_name = 'comments.html'

@login_required
def write_post(request):
    # If this is a POST request then process the Form data
    if request.method == 'POST':
        form = WritePostForm(request.POST)
        if form.is_valid():
            # create post object and save
            post = Post(title=form.cleaned_data['title'], writer=request.user, content=form.cleaned_data['content'])
            post.save()

        # return to show the post
        return HttpResponseRedirect(reverse('post', args=[post.id]))
    else:
        form = WritePostForm()

    return render(request, 'write_post.html', context={'form':form})