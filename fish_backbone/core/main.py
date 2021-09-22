import paddlex as pdx
import numpy as np
import os
import cv2

def prediction(image_path):
    test_jpg = image_path
    model = pdx.load_model('./inference_model')
    result = model.predict(test_jpg)
    result_categroy = result[0]["category"]
    return result_categroy

def prediction_seg(dataset):
    x = dataset[0].replace('\\', '/')
    file_name = dataset[1]
    model = pdx.deploy.Predictor('./inference_model_seg')
    label = model.predict(x)['label_map']
    label = label * 255
    label = label.astype(np.int)
    cv2.imwrite(f'./tmp/mask/{file_name}.png', label,
                (cv2.IMWRITE_PNG_COMPRESSION, 0))

def pre_process(data_path):
    file_name = os.path.split(data_path)[1].split('.')[0]
    return data_path, file_name

def last_process(file_name):
    image = cv2.imread(f'./tmp/image/{file_name}')
    mask = cv2.imread(f'./tmp/mask/{file_name}', 0)
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(image, contours, -1, (0, 255, 0), 2)
    cv2.imwrite('./tmp/draw/{}'.format(file_name), image)


if __name__ == '__main__':
    pass
