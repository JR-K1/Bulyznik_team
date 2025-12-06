from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('level/<int:level_number>/', views.level_detail, name='level_detail'),
    path('level/<int:level_number>/practice/', views.level_practice, name='level_practice'),
    path('level/<int:level_number>/test/', views.level_test, name='level_test'),  # ← НОВЫЙ
    path('api/filter-minerals/', views.filter_minerals, name='filter_minerals'),
    path('api/level/<int:level_number>/submit-test/', views.submit_test, name='submit_test'),  # ← НОВЫЙ

    path('level/2/lab/', views.lab_level_2, name='lab_level_2'),
]