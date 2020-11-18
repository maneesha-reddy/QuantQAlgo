from django.urls import path
from .views import ImageCreateView, Nefti, index
from . import views
urlpatterns = [
    # path('backtest/', BackTest.as_view()),
    # path('create/', ImageCreateView.as_view()),
    # path('dashboard/', Nefti.as_view()),
    path('', views.index, name='index')
]
