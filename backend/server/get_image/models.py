#from django.db import models

# Create your models here.
#from api_etalon.models import EtalonBase

import numpy as np
import torch
from torchvision import transforms
from get_image.apps import GetImageConfig

mean  = GetImageConfig.mean
std   = GetImageConfig.std
model = GetImageConfig.model
embs  = GetImageConfig.emb_list
print('mean:', mean)
print('std :', std)
print('embs:', len(embs))

def get_emb(image):   
    transform = transforms.Compose([
#        transforms.ToTensor(), 
        transforms.Resize((224)),        
        transforms.CenterCrop((224)),
        transforms.ToTensor(), 
        transforms.Normalize(mean=mean, std=std), ])
    image = transform(image).unsqueeze(0)
    print('img_shape:', image.shape)

    y = model(image).data.reshape(512)   
    print('emb_shape:', y.shape)  
    print('net response:')
    print(y[0:6], '...')
    return y

def emb_output(emb):
    emb =np.array(emb)
    dist_list = []
    for i in range(len(embs)):   
        tmp = abs(embs[i] - emb).sum()/float(len(embs))
        dist_list.append(tmp)   
    idx = np.argsort(dist_list)
    val = np.sort(dist_list)
    return idx, val

