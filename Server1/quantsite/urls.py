from django.contrib import admin
from django.urls import path, re_path, include

from django.conf.urls import url
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('website/', include('app.urls')),
    path('', views.index, name='index'),
    re_path(r'.*', views.index)
]
# urlpatterns += re_path(r'.*', views.index)
