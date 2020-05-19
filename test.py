import time
import base64
from PIL import Image
from io import BytesIO
import concurrent.futures
from predict_captcha import predict

def base64_to_image(base64_str):
    byte_data = base64.b64decode(base64_str)
    image_data = BytesIO(byte_data)
    img = Image.open(image_data)
    return img

def test(test_data):
    label = [i[0] for i in test_data]
    img = [i[1] for i in test_data]
    with concurrent.futures.ProcessPoolExecutor() as executor:
        pred = [val for val in executor.map(predict, img)]
        
    l = len(label)
    correct = 0
    for i in range(l):
        correct += (label[i]==pred[i])
    acc = correct / l
    print(f'{l} Samples\nAccuracy: {acc:.3f}')

if __name__ == '__main__':
    __spec__ = "ModuleSpec(name='builtins', loader=<class '_frozen_importlib.BuiltinImporter'>)"
    with open('test\\mixed_captcha_base64.txt') as f:
        test_data = [i.replace('\n', '').split(':')[1:] 
                     for i in f.readlines() if i[0]=='1']
        for i in range(len(test_data)):
            test_data[i][1] = base64_to_image(test_data[i][1])
    test(test_data)