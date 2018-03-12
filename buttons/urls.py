from django.urls import include, path
from . import views


app_name = "buttons"

urlpatterns = [
    path('', views.buttons, name='buttons'),
    # path('index.html', views.index, name='index')
]