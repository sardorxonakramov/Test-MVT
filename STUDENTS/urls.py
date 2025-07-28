from django.urls import path
from . import views

app_name = 'students'

urlpatterns = [
    path('', views.enter_test_code, name='enter_test_code'),
    path('start/<int:test_id>/<int:attempt_number>/', views.start_test, name='start_test'),
    path('result/<int:test_id>/<int:attempt_number>/', views.test_result, name='test_result'),
]
