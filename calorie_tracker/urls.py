from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add_food_item, name='add_food_item'),
    path('remove/<int:item_id>/', views.remove_food_item, name='remove_food_item'),
    path('reset/', views.reset_calories, name='reset_calories'),
    path('api/weekly-summary/', views.weekly_summary_api, name='weekly_summary_api'),
]