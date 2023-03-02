# coding=utf-8 

import requests
from sys import argv
import os, shutil, io
import numpy as np
from zipfile import ZipFile
from PIL import Image
import matplotlib.pyplot as plt

path = 'http://127.0.0.1:8000/icons/'

# Загрузка изображения
image_in = argv[1]
current_path  = os.getcwd()
print('current_path :', current_path) 

# Отправка изображения
print('Отправка изображения')
print(image_in)
with open(image_in, 'rb') as image:
    resp = requests.post(
        url     = path + 'api_image/',
        files   = {'image': image})    

# Ответ сервера
print('Ответ сервера')
print(resp)
image_files     = resp.content
image_values    = resp.headers['value']
image_filenames = resp.headers['filename']

values = []
for x in image_values[1:-1].split(', '):
    print(x)
    values.append(float(x))

path_to_svg = []
path_to_jpg = []
print('-----------------------------')
for i in range(6):
     tmp = 'server_response/' + image_filenames[1:-1].split(', ')[i][1:-1]
     path_to_svg.append(tmp)
     print(i, tmp)
print()
for i in range(6,12):
     tmp = 'server_response/' + image_filenames[1:-1].split(', ')[i][1:-1]
     path_to_jpg.append(tmp)
     print(i-6, tmp)

try: shutil.rmtree('server_response')
except: pass

with ZipFile(io.BytesIO(image_files), 'r') as zf:
    zf = ZipFile(io.BytesIO(image_files), 'r')
    zf.extractall(path='server_response')    
#--------------------------------------------
k = 6
plt.rc('font', size=9)
plt.figure(figsize=(14,5))
plt.subplot(2,k,1)

img = Image.open(image_in).convert('RGB')
plt.imshow(np.array(img))

for i in range(k):
    path = path_to_jpg[i]
    plt.subplot(2,k,k+1+i)
    img = Image.open(path).convert('RGB')
    plt.title(str(round(values[i],5)))
    plt.imshow(np.array(img))
img.close()
plt.pause(5)
plt.close('all')

w = ''
for i, x in enumerate(path_to_svg):
    w += str(i+1) +'  ' + x +'\n'
with open('server_response/text.txt', 'w') as f:
    f.write(w)


