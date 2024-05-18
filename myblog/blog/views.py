from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.views import generic
from datetime import datetime    
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
        context['error'] = False
        # Form for adding new comments
        context['form'] = LeaveCommentForm()
        return context
    
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = LeaveCommentForm(request.POST)
            id = int(self.kwargs.get('pk'))
            if form.is_valid():
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
    
    def get_context_data(self, **kwargs):
        # Inherit previous get_context_data function
        context = super(CommentListView, self).get_context_data(**kwargs)
        # Form for adding new comments
        context['form'] = LeaveCommentForm()
        return context
    
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = LeaveCommentForm(request.POST)
            id = int(self.kwargs.get('pk'))
            if form.is_valid():
                comment = Comment(
                    post=Post.objects.get(id=id), 
                    writer=request.user, 
                    content=form.cleaned_data['content']
                    )
                comment.save()
            return HttpResponseRedirect(reverse('comments', args=[id]))

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

@login_required
def like(request, model, id, like):
    if like == "1": like = True
    elif like == "0": like = False
    else: raise Http404("Invalid Request.")

    try:
        if model == "post":
            post = Post.objects.get(id=id)
            try: 
                post_like = PostLike.objects.get(post=post, user=request.user)
                if post_like.like: post_like.like = False
                else: post_like.like = True
            except:
                post_like = PostLike(post=post, user=request.user)
            post_like.save()
            post.likes = PostLike.objects.filter(post=post, like=True).count()
            post.save()
            return  HttpResponseRedirect(reverse('post', args=[id]))

        elif model == "comment":
            comment = Comment.objects.get(id=id)
            try:
                comment_like = CommentLike.objects.get(comment=comment, user=request.user)
                if like:
                    if comment_like.like == 1: comment_like.like = 0
                    else: comment_like.like = 1
                elif not like:
                    if comment_like.like == -1: comment_like.like = 0
                    else: comment_like.like = -1
            except:
                if like:
                    comment_like = CommentLike(comment=comment, user=request.user, like=1)
                elif not like:
                    comment_like = CommentLike(comment=comment, user=request.user, like=-1)
            comment_like.save()
            comment.likes = CommentLike.objects.filter(comment=comment, like=1).count()
            comment.dislikes = CommentLike.objects.filter(comment=comment, like=-1).count()
            comment.save()
            return  HttpResponseRedirect(reverse('post', args=[comment.post.id]))
        else:
          raise Http404("Invalid Request.")
    except:
        raise Http404("Invalid Request.") 

def search(request):
    context = {}
    posts = []
    if request.method == 'POST':
        q = request.POST.get('search_query').split()
        context['keywords'] = ", ".join(q)
        for x in q:
            for post in Post.objects.all():
                if (x in post.title or x in post.writer) and post not in posts: 
                    posts.append(post)
    context['posts'] = posts
    return render(request, 'search.html', context=context)

@login_required
def edit_post(request, pk):
    if request.method == 'POST':
        form = WritePostForm(request.POST)
        if form.is_valid():
            # edit post object and save
            post = Post.objects.get(id=pk)
            post.title = form.cleaned_data['title']
            post.content=form.cleaned_data['content']+datetime.now().strftime('\n (edited on %Y-%m-%d %H:%M)')
            post.save()
        # return to show the post
        return HttpResponseRedirect(reverse('post', args=[post.id]))
    else:
        try:
            p = Post.objects.get(id=pk)
            if request.user.username == p.writer:
                form = WritePostForm(initial={'title':p.title, 'content':p.content})
            else: raise Http404("Invalid Request.")
        except:
            raise Http404("Invalid Request.")

    return render(request, 'write_post.html', context={'form':form})

@login_required
def edit_comment(request, pk):
    if request.method == 'POST':
        form = LeaveCommentForm(request.POST)
        if form.is_valid():
            # edit comment object and save
            comment = Comment.objects.get(id=pk)
            comment.content=form.cleaned_data['content']+datetime.now().strftime('\n (edited on %Y-%m-%d %H:%M)')
            comment.save()
        # return to show the post
        return HttpResponseRedirect(reverse('post', args=[comment.post.id]))
    else:
        try:
            c = Comment.objects.get(id=pk)
            if request.user.username == c.writer:
                form = LeaveCommentForm(initial={'content':c.content})
            else: raise Http404("Invalid Request.")
        except:
            raise Http404("Invalid Request.")

    return render(request, 'write_post.html', context={'form':form})