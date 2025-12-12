from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # Маршруты для уровней
    path('level/<int:level_number>/', views.level_detail, name='level_detail'),
    path('level/<int:level_number>/practice/', views.level_practice, name='level_practice'),
    path('level/<int:level_number>/test/', views.level_test, name='level_test'),
    # Специальный маршрут для 2 уровня
    path('lab/level2/', views.lab_level_2, name='lab_level_2'),
    # API маршруты
    path('api/filter-minerals/', views.filter_minerals, name='filter_minerals'),
    path('api/submit-test/<int:level_number>/', views.submit_test, name='submit_test'),
]