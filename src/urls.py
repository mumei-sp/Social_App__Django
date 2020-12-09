from django.contrib import admin
from django.urls import path,include
from .views import home_view

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
	path("",home_view,name="home"),
    path('admin/', admin.site.urls),
    path("profile/",include("profiles.urls")),
    path("posts/",include("posts.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)