from django.urls import path
from .views import ImageCreateView
urlpatterns = [
    # path('backtest/', BackTest.as_view()),
    path('create/', ImageCreateView.as_view()),
]
