from django.urls import path
from . import views
app_name = 'character'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('admin/', views.AdminView.as_view(), name='admin'),
    path('<int:character_id>/save/', views.save, name='save'),
    path('<int:pk>/buyskills/', views.CharacterSkillsCreate.as_view(), name='buyskills'),
    path('new/', views.CharacterCreate.as_view(),name='new_char')
]
