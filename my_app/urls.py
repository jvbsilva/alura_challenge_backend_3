from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('login/', views.login, name = 'login'),
    path('logout/', views.logout, name = 'logout'),
    path('cadastro/', views.cadastro, name = 'cadastro'),
    path('imports/', views.imports, name = 'imports'),
    path('list_transactions/<str:date_transactions>',views.list_transactions,name="list_transactions"),
    path('usuarios/', views.usuarios, name = 'usuarios'),
    path('create_user/', views.create_user, name = 'create_user'),
    path('update_user/<str:user_pk>',views.update_user,name="update_user"),
    path('delete_user/<str:user_pk>',views.delete_user,name="delete_user"),
]