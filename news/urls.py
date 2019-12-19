from django.urls import path
from . import views
app_name = 'news'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('news/<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('news/', views.IndexView.as_view(), name='index1'),
    path('news/<slug:slug>/', views.DetailView.as_view(), name='detail_slug')
]
