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
from django.urls import path, include
from . import views

urlpatterns = [

    # path('', views.home, name='blog-home'),
    path('', views.DealListView.as_view(), name='deals-home'),
    # path('deal/<int:pk>/', views.DealDetailView.as_view(), name='deal-detail'),
    path('deal/<int:pk>/', views.DealDetailView, name='deal-detail'),

    path('deal/new/', views.DealCreateView.as_view(), name='deal-create'),
    path('deal/<int:pk>/update/', views.DealUpdateView, name='deal-update'),
    # path('deal/<int:pk>/update/', views.DealUpdateView.as_view(), name='deal-update'),
    path('deal/<int:pk>/delete/', views.DealDeleteView, name='deal-delete'),
    # path('post/<int:pk>/delete/', views.DealDeleteView.as_view(), name='deal-delete'),
    path('user/<str:username>', views.UserDealPostListView.as_view(), name='user-deals'),

    

]
