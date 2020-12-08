from django.urls import path
from .views import ImageCreateView
from . import views
urlpatterns = [

    path('create/', ImageCreateView.as_view()),
    # path('dashboard/', Nefti.as_view()),
    path('papertrade/', views.papertrade, name='paper')
]
