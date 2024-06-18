from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('', views.recipe_list, name='recipe_list'),  # Zde upravujeme URL pro seznam receptů
    path('add/', views.add_recipe, name='add_recipe'),
    path('logout/', views.user_login, name='logout'),
]