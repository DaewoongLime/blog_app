from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.views import generic
from .models import *
from .forms import *

class PostListView(generic.ListView):
    model = Post # Set reference model
    context_object_name = 'posts' # Set name used in template for model reference
    template_name = 'home.html' # Specify template name and directory
    paginate_by = 5 # Default pagination tool

class PostDetailView(generic.DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'view_post.html'

    def get_context_data(self, **kwargs):
        # Inherit previous get_context_data function
        context = super(PostDetailView, self).get_context_data(**kwargs)
        # Filter comments to show in respective posts
        comments = Comment.objects.filter(post=int(self.kwargs.get('pk')))
        # Show only the top 5 comments sorted by number of likes
        comments.order_by('-likes')[:5]
        context['comments'] = comments
        # Form for adding new comments
        context['form'] = LeaveCommentForm()
        return context
    
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = LeaveCommentForm(request.POST)
            if form.is_valid():
                id = int(self.kwargs.get('pk'))
                comment = Comment(
                    post=Post.objects.get(id=id), 
                    writer=request.user, 
                    content=form.cleaned_data['content']
                    )
                comment.save()

                return HttpResponseRedirect(reverse('post', args=[id]))

class CommentListView(generic.ListView):
    model = Comment
    context_object_name = 'comments'
    template_name = 'comments.html'

    def get_queryset(self): 
        return Comment.objects.filter(post=self.kwargs['pk'])

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

def profile(request, user):
    try:
        get_user_model().objects.get(username=user)
    except:
        raise Http404("Profile does not Exist.") 

    context = {
        'name':user,
        'posts':Post.objects.filter(writer=user),
        'comments':Comment.objects.filter(writer=user),
        'auth':False,
    }

    if user == request.user.username:
        context['auth'] = True

    return render(request, 'profile.html', context=context)

@login_required
def delete(request, pk, model):
    try:
        if model == 'post':
            post = Post.objects.get(id=pk, writer=request.user.username)
            post.delete()
        elif model == 'comment':
            comment = Comment.objects.get(id=pk, writer=request.user.username)
            comment.delete()
        else:
            raise Http404("Invalid Request.") 
    except:
        raise Http404("Invalid Request.") 

    return render(request, 'deleted_successfully.html')

def show_all(request, user, model):
    context = {'auth':False}
    if user == request.user.username:
        context['auth'] = True
    try:
        if model == 'posts':
            context['model'] = 'Posts'
            context['objects'] = Post.objects.filter(writer=user)
        elif model == 'comments':
            context['model'] = 'Comments'
            context['objects'] = Comment.objects.filter(writer=user)
        else:
            raise Http404("Invalid Request.") 
    except:
        raise Http404("Invalid Request.") 

    return render(request, 'show_all.html', context=context)
    