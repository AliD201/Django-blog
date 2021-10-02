"""django_blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from django.contrib.auth import views as auth_views
from users import views as user_views
from users.forms import EmailValidationOnForgotPassword
urlpatterns = [
    path('', include('blog.urls')),
    path('deals/', include('deal.urls')),

    
    path('admin/', admin.site.urls),
    path('register/', user_views.register_backend, name = 'register'),
    # path('register/', user_views.register, name = 'register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html',redirect_authenticated_user=True), name = 'login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name = 'logout'),
    path('profile/', user_views.profile, name = 'profile'),
    path('password-reset/',
    # this page doesn't send errors if the email doesn't exist 
    user_views.MyPasswordResetView
    .as_view(template_name='users/password_reset.html', form_class=EmailValidationOnForgotPassword), name = 'password_reset'),
    path('password-reset-done/',
    user_views.MyPasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name = 'password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',user_views.MyPasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), name = 'password_reset_confirm'),
    path('password-reset-complete/',
    user_views.MyPasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name = 'password_reset_complete'),


    # Rest FRAME WORK 
    path('api/users/', include('users.api.urls', 'users_api')),

    #simple jwt
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

