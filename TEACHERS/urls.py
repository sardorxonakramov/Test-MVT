from django.urls import path
from . import views
app_name = 'teachers'

urlpatterns = [
    path("tests/", views.test_list, name="test_list"),
    path("tests/create/", views.test_create, name="test_create"),
    path("tests/<int:pk>/edit/", views.test_update, name="test_update"),
    path("tests/<int:pk>/delete/", views.test_delete, name="test_delete"),
    path('tests/<int:pk>/', views.test_detail, name='test_detail'),
    path('tests/<int:test_id>/questions/add/', views.add_question, name='add_question'),
    path('questions/<int:pk>/edit/', views.edit_question, name='edit_question'),
    path('questions/<int:pk>/delete/', views.delete_question, name='delete_question'),
]
