from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.contrib.auth.views import LogoutView


app_name = 'home'
urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('auth/', include('authentication.urls')),
    path('posts/', include('posts.urls')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
