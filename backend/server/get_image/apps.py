#from django.apps import AppConfig

#class GetImageConfig(AppConfig):
#    default_auto_field = 'django.db.models.BigAutoField'
#    name = 'get_image'
    
    
from django.apps import AppConfig
import torch, pickle

class GetImageConfig(AppConfig):
    name = 'get_image'
    
    path  = 'net_models/ResNet18_emb.pth'
    model = torch.load(path)

    mean = torch.FloatTensor([0.485, 0.456, 0.406])
    std  = torch.FloatTensor([0.229, 0.224, 0.225])

    with open('net_models/images.pickle', 'rb') as f:
        images = pickle.load(f)
    jpg_list = []
    svg_list = []
    emb_list = []
    for jpg, svg, emb in images:
        jpg_list.append(jpg)
        svg_list.append(svg)
        emb_list.append(emb)
        

