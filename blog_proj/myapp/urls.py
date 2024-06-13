from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("home/", views.home, name="home"),
    path("", views.home, name="main"),
    path('about/', views.about, name='about'),  # Route for the about page
    path('contact/', views.contact, name='contact'),
    path('editor/', views.editor, name='editor'),
    path('blog/', views.blog, name='blog'),
    path('user_login/', views.user_login, name='user_login'),
    path('blog_detail/', views.blog_detail, name='blog_detail'),
    path('register/', views.register, name='register'),
    path('blog/<int:pk>/', views.blog_detail, name='blog_detail'),
    path('blog/<int:pk>/edit/', views.blog_edit, name='blog_edit'),
    path('user_logout/', auth_views.LogoutView.as_view(next_page='user_login'), name='user_logout'),
    path('post/<int:pk>/delete/', views.post_delete, name='post_delete'),
    path('blog/<int:pk>/post_confirm_delete/', views.post_delete, name='post_confirm_delete'),
]
