from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns
from django.contrib.auth import views as django_auth_views
from auth_app import views as auth_views

urlpatterns = [
    path('', auth_views.home, name='home'),
    path('admin/', admin.site.urls),
    path('edit-profile/', auth_views.edit_profile, name='edit-profile'),
    # AUTH
    path('register/', auth_views.register, name='register'),
    path('login/', django_auth_views.LoginView.as_view(template_name='auth_app/login.html'), name='login'),
    path('logout/', django_auth_views.LogoutView.as_view(template_name='auth_app/logout.html'), name='logout'),
    # password reset
    path('password-reset/',
         django_auth_views.PasswordResetView.as_view(template_name='auth_app/password_reset.html'),
         name='password_reset'),
    path('password-reset/done/',
         django_auth_views.PasswordResetDoneView.as_view(template_name='auth_app/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         django_auth_views.PasswordResetConfirmView.as_view(template_name='auth_app/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         django_auth_views.PasswordResetCompleteView.as_view(template_name='auth_app/password_reset_complete.html'),
         name='password_reset_complete'),
    # posts
    path('post/', include('posts_app.urls')),

]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
