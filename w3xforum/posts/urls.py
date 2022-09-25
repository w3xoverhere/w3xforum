from django.urls import path, include
from . import views

app_name = "posts"
urlpatterns = [
    path('', views.PostsList.as_view(), name="posts_list"),
    path('add/', views.post_add, name="post_add"),
    path('<slug:category_slug>/<int:post_pk>/', views.PostDetail.as_view(), name="post_detail"),
    path('categories/', views.CategoryList.as_view(), name="categories_list"),
    path('<slug:category_slug>/', views.category_detail, name="category_detail"),
]
