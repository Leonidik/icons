# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators    import api_view
from django.http import FileResponse
from zipfile     import ZipFile

from get_image.apps    import GetImageConfig
from get_image.models  import get_emb, emb_output

from os  import getcwd     as getcwd
from io  import BytesIO    as BytesIO
from PIL import Image

embs = GetImageConfig.emb_list
jpgs = GetImageConfig.jpg_list
svgs = GetImageConfig.svg_list

@csrf_exempt 
@api_view(['POST'])
def view_api_image(request):
#    print(request.META)
    print('========================================')  
    print(getcwd())    
    print('LOGNAME    : ', request.META['LOGNAME'])      
    print('SERVER_NAME: ', request.META['SERVER_NAME'])
    print('REMOTE_ADDR: ', request.META['REMOTE_ADDR'])   
    print('HTTP_HOST  : ', request.META['HTTP_HOST'])
    user_ip   = request.META['REMOTE_ADDR']     
    user_id   = request.user.id
    server_ip = request.META['HTTP_HOST']
    print('username:', request.user) 
    print('user_ip :', user_ip)  
    print('-----------------------------------')
    img = request.data['image']      
    image = Image.open(BytesIO(img.read()))
    image = image.convert('RGB')
    img.close()
    print(type(image))
    print('format:', image.format)
    print('size  :', image.size)
    print('mode  :', image.mode)
    print('-----------------------------------')    
    emb = get_emb(image)
    print('-----------------------------------')      
    print('перечень кандидатов:')   
    idx, val = emb_output(emb)
    jpg_list  =[]
    svg_list = []
    val_list = val 
           
    jpg_list = ['media/icon_jpg/'+jpgs[i] for i in idx][0:6]
    svg_list = ['media/icon_svg/'+svgs[i] for i in idx][0:6]
    val_list = [round(val[i],5) for i in range(6)]
    for i in range(6):
        print('{0:2.5f}  {1}'.format(val_list[i], svg_list[i]))                    
    print('server response:')
    print(val_list)
    print(jpg_list[0:2])     
    print(svg_list[0:2])
    print('---------------------------------------------')
    buf = BytesIO()   
    with ZipFile(buf, 'a') as myzip:
        for x in svg_list + jpg_list:
            myzip.write(x)    
    buf.seek(0)     
    response = FileResponse(buf)
    response['value']    = val_list
    response['filename'] = svg_list + jpg_list  

    return response


