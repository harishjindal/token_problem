from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('generate/',views.generate_token, name='generate_token'),
    path('keep_alive/',views.keep_alive, name='keep_alive'),
    path('delete/',views.delete_token, name='delete_token')
]