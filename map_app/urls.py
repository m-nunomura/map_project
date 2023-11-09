"""
URL configuration for map_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from . import views
from django.urls import path

app_name = "map"

urlpatterns = [
    path("", views.index, name="index"),
    path("create/quake/",views.create_quake,name="create_quake"),
    path("update/<int:pk>/address/",views.address_update, name="address_update"),
    path("update/<int:pk>/store/",views.store_update, name="store_update"),
    path("delete/<int:pk>/address/",views.address_delete, name="address_delete"),
    path("delete/<int:pk>/store/",views.store_delete, name="store_delete"),
]
