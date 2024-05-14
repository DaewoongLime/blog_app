from django.contrib import admin
from .models import *

# Register your models here.
class CommentInline(admin.TabularInline):
    model = Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'writer')
    list_filter = ('date','likes')
    fields = ['title', 'writer', 'content', ('date', 'likes')]

    inlines = [CommentInline]

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'writer')
    list_filter = ('date', 'likes', 'dislikes')
    fieldsets = (
        (None, {'fields': ('post', 'writer', 'content', 'date')}),
        ('Likeness', {'fields': ('likes', 'dislikes')})
    )

@admin.register(PostLike)
class PostLikeAdmin(admin.ModelAdmin):
    list_display = ('post', 'user')

@admin.register(CommentLike)
class CommentLikeAdmin(admin.ModelAdmin):
    list_display = ('comment', 'user')