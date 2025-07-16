from django.urls import path
from . import views

urlpatterns = [
    path('', views.entry_list, name='entry_list'),
    path('new/', views.create_entry, name='create_entry'),
    path('entry/<int:entry_id>/', views.entry_detail, name='entry_detail'),

    #editing and deleting urls
    path('entry/<int:entry_id>/edit/', views.edit_entry, name='edit_entry'),
    path('entry/<int:entry_id>/delete/', views.delete_entry, name='delete_entry'),
    path('mood-stats/', views.mood_stats, name='mood_stats'),
    path('analytics/', views.analytics_page, name='analytics'),

]
