from django.urls import path
from . import views

urlpatterns = [
    path('', views.PostListView.as_view(), name='home'),
    path('<int:pk>/', views.PostDetailView.as_view(), name="post"),
    path('<int:pk>/comments/', views.CommentListView.as_view(), name="comments"),
    path('write/', views.write_post, name="write-blog"),
]