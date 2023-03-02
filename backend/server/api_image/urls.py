# api_etalon URLs Configuration

from django.urls import path
from .views import view_api_image
     
urlpatterns = [
   path('', view_api_image, name = 'qqq.html'), 

]



