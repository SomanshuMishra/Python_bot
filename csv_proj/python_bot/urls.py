"""csv_proj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path , include
from python_bot import views
from python_bot.views import Source_file , Compare_file
urlpatterns = [
    path('',views.index,name='index'),
    path('u/',Source_file.as_view()),
    path('d/',Compare_file.as_view()),
    path('compare/',views.compare,name='compare'),
    path('destination_list/',views.show_all_destination_files,name='show_all_destination_files'),
    path('source_list/',views.show_all_source_files,name='show_all_source_files'),
    path('delete_source/',views.delete_source,name='delete_source'),
    path('delete_destination/',views.delete_destination,name='delete_destination'),

    path('try/',views.try_func,name='try_func')
]
