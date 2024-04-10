import cv2
import numpy as np
from lib import for_image as ilib

if __name__ == '__main__':
    color = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
    original_img = cv2.imread('./img/5120.tif')
    region_img = cv2.imread('./img/kessyou_region.jpg')

    print(f'original:{np.shape(original_img)}, predict:{np.shape(region_img)}')

    img_width, img_height, channels = region_img.shape[:3]
    cut_size = 32
    region_list = [[-1] * int(img_width/cut_size) for i in range(int(img_height/cut_size))]

    for i in range(int(img_height/cut_size)):
        for j in range(int(img_width/cut_size)):
            y = i * cut_size
            x = j * cut_size
            predict_color = ilib.color_checker(region_img[y:y+cut_size, x:x+cut_size], i, j, cut_size, 'predict')
            region_list[i][j] = predict_color
    
    region_list = ilib.remove_one_dot(region_list)

    for i in range(int(img_height/cut_size)):
        for j in range(int(img_width/cut_size)):
            y = i * cut_size
            x = j * cut_size
            pt1 = (x, y)
            pt2 = (x+cut_size, y+cut_size)
            cv2.rectangle(region_img, pt1, pt2, color[region_list[i][j]], cv2.FILLED)
    
    combine_img = cv2.addWeighted(region_img, 0.3, original_img, 0.7, 0, dtype = cv2.CV_32F)
    cv2.imwrite('./img/kessyou_region_remove.jpg', region_img)
    cv2.imwrite('./img/kessyou_result_remove.jpg', combine_img)