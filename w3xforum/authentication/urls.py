from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

app_name = "auth"
urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('register/', views.user_registration, name='register'),
    path('register/activation/<str:user_name>/', views.user_activation, name='activation'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
