import os
from PIL import Image


import os
path = 'new_xin/'
i = 1
for file in os.listdir(path):
    if os.path.isfile(os.path.join(path,file))==True:
        filename = path + file
        print(filename)
        img = Image.open(filename)
        newname = f'direction{i}.png'
        i += 1
        img.save(newname)