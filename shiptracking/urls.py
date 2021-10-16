"""shiptracking URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from tracking.views import *
from django .contrib.admin.sites import AdminSite

a = path('accounts/profile/', customer_view.as_view(), name='customer')
#b = path('customer/', customer_view, name='customer')


urlpatterns = [

    path('adminfreak/', admin.site.urls),
    path('', home_view, name='home'),
    path('accounts/signup/<str:id>/', AccountSignupView.as_view(), name='account_signup'),
    #path('accounts/login/', customer_view, name='account_login'),
    a,
    path('update/', updatecustomer, name='updatecustomer'),
    path('pricing/', pricing, name='pricing'),
    path('page_error/', error_404_view, name='invalid_view'),
    path('res_page/', res_page, name='res_page'),
    #path('accounts/profile/', customer_view, name='customer'),

    path('accounts/', include('allauth.urls')),
    path('create_cust_container/<int:id>/', create_cust_container_view, name='create_cust_container'),
    #path('customer/<uidb64>/', customer_view, name='customer'),
]

handler404 = 'tracking.views.error_404_view'
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

