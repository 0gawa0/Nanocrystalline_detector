import cv2
import numpy as np
import copy
from .lib import for_image as ilib

if __name__ == '__main__':
    predict_img = cv2.imread('img/kessyou_region_remove.jpg')
    annotate_img = cv2.imread('img/kessyou.jpg')

    img_width, img_height, channels = predict_img.shape[:3]
    cut_size = 32
    print(f'{img_width}, {img_height}')
    predict_region_list = [[-1] * int(img_width/cut_size) for i in range(int(img_height/cut_size))]
    annotate_list = copy.deepcopy(predict_region_list)
    test = copy.deepcopy(annotate_img)

    # 精度算出の対象とするクラス（0：縞模様、1：縞なし、2：対象外）
    color_num = 0
    predict_count = 0
    annotate_count = 0
    true_and_true = 0

    for i in range(int(img_height/cut_size)):
        for j in range(int(img_width/cut_size)):
            y = i * cut_size
            x = j * cut_size
            pt1 = (x, y)
            pt2 = (x+cut_size, y+cut_size)

            predict_color = ilib.color_checker(predict_img[y:y+cut_size, x:x+cut_size], i, j, cut_size, 'predict')
            annotate_color = ilib.color_checker(annotate_img[y:y+cut_size, x:x+cut_size], i, j, cut_size, 'annotate')

            predict_region_list[i][j] = predict_color
            annotate_list[i][j] = annotate_color

            print(f'{predict_color}, {annotate_color}')

            if predict_region_list[i][j] == color_num:
                predict_count += 1
            if annotate_list[i][j] == color_num:
                annotate_count += 1
            if predict_region_list[i][j] == color_num and annotate_list[i][j] == color_num:
                true_and_true += 1
                cv2.rectangle(test, pt1, pt2, (170, 255, 0), cv2.FILLED)

    recall = true_and_true/annotate_count
    precision = true_and_true/predict_count
    f1 = 2 * recall * precision / (recall + precision)
    print(f'{annotate_count}, {predict_count}, {true_and_true}')
    print(f'recall: {recall}, precision: {precision}, f1:{f1}')
    cv2.imwrite('./img/calc_result_check.jpg', test)