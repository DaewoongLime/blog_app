from django.urls import path
from . import views

urlpatterns = [
    path('', views.PostListView.as_view(), name='home'),
    path('<int:pk>/', views.PostDetailView.as_view(), name="post"),
    path('<int:pk>/del/<str:model>/', views.delete, name="delete"),
    path('<int:pk>/comments/', views.CommentListView.as_view(), name="comments"),
    path('write/', views.write_post, name="write-blog"),
    path('<str:user>/profile/', views.profile, name="user-profile"),
    path('<str:user>/show_all/<str:model>/', views.show_all, name="show-all"),
    path('like/<str:model>/<int:id>/<str:like>/', views.like, name="like"),
    path('search/', views.search, name="search"),
    path('<int:pk>/edit/', views.edit_post, name="edit-post"),
    
]