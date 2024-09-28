from django.urls import include, path
from .views import login_view,Registerview


urlpatterns = [
    path('login/',login_view,name='login'),
    path('register/',Registerview.as_view(),name='register'),
    
]
