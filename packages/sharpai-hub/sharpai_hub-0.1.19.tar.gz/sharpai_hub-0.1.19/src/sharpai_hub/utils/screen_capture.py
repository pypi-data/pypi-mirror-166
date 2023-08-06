import os
import platform
import time
import requests
from PIL import ImageGrab

#The output of platform.system() is as follows:

# Linux: Linux
# Mac: Darwin
# Windows: Windows

system = platform.system()

def screen_capture(save_path):
    img = None
    try:
        if system == 'Linux':
            img = ImageGrab.grab(xdisplay="")
        else:
            img = ImageGrab.grab()
    except Exception as e:
        print(e)
        return None
    if img == None:
        return None
    rgb_img = img.convert('RGB')
    filename = 'img.jpg'
    src_file_path =  os.path.join(save_path,filename)
    detector_filepath=  os.path.join('/opt/nvr/detector/images', filename)
    rgb_img.save(src_file_path)
    return detector_filepath

if __name__ == '__main__':
    while True:
        detector_filepath = screen_capture('/home/simba/AI_OS/laptop_monitor/images/img.jpg')
        r = requests.post('http://localhost:3000/submit/image', json={"filename": detector_filepath, 'camera_id':'screen'})
        time.sleep(10)
