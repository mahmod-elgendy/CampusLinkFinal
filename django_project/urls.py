"""django_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from users import views as user_views
from users import views



urlpatterns = [
    path('blog/', include('blog.urls')),
    path('admin/', admin.site.urls),
    path('register/', views.register, name='register'),
    path('login/register/', views.register, name='register'),

    path('mentors/', views.mentors, name='mentors'),
    path('profile/mentors/', views.mentors, name='mentors'),
    path('profile/hero/mentors/', views.mentors, name='mentors'),

    path('notification/', views.notification, name='notification'),
    path('profile/notification/', views.notification, name='notification'),
    path('profile/hero/notification/', views.notification, name='notification'),



    path('', views.index, name='index'),  # Single home view

    path('post/create/', views.create_post, name="create_post"),
    path("post/edit/<str:post_id>/", views.edit_post, name="edit_post"),
    path("post/delete/<str:post_id>/", views.delete_post, name="delete_post"),  # Consistent delete_post pattern
    path('register/', views.register, name='register'),

    path("login/", views.login, name="login"),

    path("hero/", views.timeline, name="timeline"),
    path("profile/hero/", views.timeline, name="timeline"),

    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),

    path('profile/', views.get_user_profile_query, name='get_user_profile_query'),  # Handles query parameter
    path('profile/<str:user_id>/', views.get_user_profile_path, name='get_user_profile_path'),  # Handles path parameter
    path("profile/update_profile/ <str:user_id>", views.update_user_page, name='update_user_page'),
    path("update_profile/ <str:user_id>", views.update_user_page, name='update_user_page'),
    path('update_profile/<str:user_id>/submit/', views.update_user_profile, name='update_user_profile'),
    path('profile/update_profile/<str:user_id>/submit/', views.update_user_profile, name='update_user_profile'),
    path('profile/delete/<str:user_id>/', views.delete_user_profile, name='delete_user_profile'),
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='users/password_reset.html'
         ),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='users/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='users/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='users/password_reset_complete.html'
         ),
         name='password_reset_complete')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])