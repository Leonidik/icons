from django.shortcuts import render

# Create your views here.
import os, io
from PIL import Image
#import cv2
#import numpy as np
from .forms import ImageForm

from get_image.apps    import GetImageConfig
from get_image.models  import get_emb, emb_output

embs = GetImageConfig.emb_list
jpgs = GetImageConfig.jpg_list
svgs = GetImageConfig.svg_list

def get_image(request):
    print('=====================================') 
    print('Current Directory:', os.getcwd()) 
    print('request:', request)
    print('method :', request.method)
    print('LOGNAME    : ', request.META['LOGNAME'])      
    print('SERVER_NAME: ', request.META['SERVER_NAME'])
    print('REMOTE_ADDR: ', request.META['REMOTE_ADDR'])   
    print('HTTP_HOST  : ', request.META['HTTP_HOST'])
    user      = request.user
    server_ip = request.META['HTTP_HOST']  
    print('username:', user)
    print('----------------------------------------')    
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)            
        if form.is_valid():
           img = form.cleaned_data['image']      
           image= Image.open(io.BytesIO(img.read()))
           image = image.convert('RGB')
           img.close()
           print(type(image))
           print('format:', image.format)
           print('size  :', image.size)
           print('mode  :', image.mode)
           image.save('media/filename.jpg')        
#           image = np.frombuffer(img.read(), 'uint8')
#           image = cv2.imdecode(image, 1)   
#           print('сv2 image:', image)           
#           cv2.imwrite("media/filename.jpg", image)
           print('----------------------------------------')       
           emb = get_emb(image)
           image.close()
           print('----------------------------------------') 
           print('перечень кандидатов:')           
           idx, val = emb_output(emb)
           jpg_list  =[]
           svg_list = []
           val_list = val 
           
           jpg_list = ['/media/icon_jpg/'+jpgs[i] for i in idx][0:6]
           svg_list = ['/media/icon_svg/'+svgs[i] for i in idx][0:6]
           val_list = [round(val[i],5) for i in range(6)]
           for i in range(6):
               print('{0:2.5f}  {1}'.format(val_list[i], svg_list[i]))           

           print('----------------------------------------')                                   
           return render(request, 'get_image/image_output.html', locals( ))
    else:
        form = ImageForm() 
    return render(request, 'get_image/image_form.html', locals( ))

    
