import cv2
import numpy as np
import copy
import warnings
from .lib import for_image as ilib

if __name__ == '__main__':
    warnings.simplefilter('ignore')
    annotate_img = cv2.imread('./img/annotation_draw_line_jpg.jpg')
    
    result_img = annotate_img.copy()
    print(np.shape(annotate_img))

    color_data_list = []

    cut_size = 32
    img_width, img_height, channels = annotate_img.shape[:3]
    region_list = [[-1] * int(img_width/cut_size) for i in range(int(img_height/cut_size))]

    for i in range(int(img_height/cut_size)):
        for j in range(int(img_width/cut_size)):
            y = i * cut_size
            x = j * cut_size
            if ilib.isColor(annotate_img[x:x+cut_size, y:y+cut_size], cut_size):
                region_list[j][i] = 1
                color_data_list.append({f'({j}, {i})':annotate_img[x:x+cut_size, y:y+cut_size].tolist()})
                # print(f'x:{j} y:{i} color shape:{np.shape(annotate_img[x:x+cut_size, y:y+cut_size])}')

    for i in range(int(img_height/cut_size)):
        for j in range(int(img_width/cut_size)):
            y = i * cut_size
            x = j * cut_size
            pt1 = (x, y)
            pt2 = (x+cut_size, y+cut_size)
            if region_list[i][j] == 1:
                cv2.rectangle(annotate_img, pt1, pt2, (0, 170, 255), cv2.FILLED)
            else:
                cv2.rectangle(annotate_img, pt1, pt2, (0, 0, 0), cv2.FILLED)
    
    mask_img = cv2.cvtColor(annotate_img, cv2.COLOR_BGR2GRAY)
    contours, hierarchy = cv2.findContours(mask_img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    print(len(contours))

    filled = copy.deepcopy(annotate_img)
    for i in range(len(contours)):
        if cv2.contourArea(contours[i]) > cut_size * cut_size:
            area = cv2.fillPoly(filled, [contours[i][:,0,:]], (255, 0, 0), lineType=cv2.LINE_8, shift=0)
    
    combine_img = cv2.addWeighted(annotate_img, 0.3, result_img, 0.7, 0)
    combine_area_img = cv2.addWeighted(area, 0.3, result_img, 0.7, 0)
    cv2.imwrite('./img/result/annotate_search_result.jpg', combine_img)
    cv2.imwrite('./img/kessyou_contour.jpg', annotate_img)
    cv2.imwrite('./img/kessyou_filled.jpg', area)
    cv2.imwrite('./img/result/annotate_area_search_result.jpg', combine_area_img)
