from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('create_customer/', views.create_customer, name='create_customer'),
    path('customer_list/', views.customer_list, name='customer_list'),
    path('process_document_upload/', views.process_document_upload, name='process_document_upload'),
    path('', views.home, name='home'),
    path('customer_data/', views.customer_list_extracted, name='customer_data'),
]
