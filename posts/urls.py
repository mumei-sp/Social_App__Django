from django.urls import path
from .views import post_comment_list_view,PostDeleteView,PostUpdateView,like_unlike_post

urlpatterns=[
			path("",post_comment_list_view,name="posts"),
			path("delete_post/<int:pk>/",PostDeleteView.as_view(),name="delete_post"),
			path("update_post/<int:pk>/",PostUpdateView.as_view(),name="update_post"),
			path("liked/",like_unlike_post,name="liked"),
			]