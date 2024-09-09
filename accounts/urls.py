from django.urls import path
from accounts import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('post/', views.add_author, name='post'),
    path('create_article/', views.create_article, name='create_article'),
    path('read/', views.read, name='read'),
    path('article/<int:id>/', views.article_detail, name='article_detail'),
    path('authors/', views.author_list, name="authors"),
    path('list_articles/', views.list_article, name="articles"),
    path('delete/<int:pk>/', views.delete, name="delete"),
    path('edit/<int:pk>/', views.edit, name='edit'),
    path('delete_author/<int:pk>/', views.delete_author, name="delete_author"),
    path('forgot-password/', views.send_password_reset_email, name='forgot_password'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
]
