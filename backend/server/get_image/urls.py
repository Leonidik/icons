# get_image URLs Configuration

from django.urls import path
from .views import get_image
     
urlpatterns = [
   path('', get_image, name = 'get_image'), 

]



