import cv2
import copy
import matplotlib.pyplot as plt
from lib import line_detector as ld
from lib import for_image as ilib

if __name__ == '__main__':
    color = [
            (255, 255, 255), (242, 237, 255), (234, 226, 255),
            (220, 206, 255), (210, 193, 255), (196, 174, 255),
            (190, 164, 255), (182, 154, 255), (169, 135, 255),
            (159, 122, 255), (152, 112, 255), (144, 101, 255),
            (135, 88, 255), (127, 77, 255), (121, 69, 255),
            (113, 57, 255), (97, 36, 255), (71, 0, 255),
            ]
    kessyou_img = cv2.imread('./img/5120.tif')
    shima_region_img = cv2.imread('./img/kessyou_region_remove.jpg')

    angles = [0] * 18
    shima_count = 0

    cut_size = 32
    img_width, img_height, channels = kessyou_img.shape[:3]

    angle_positions = [[-1] * int(img_width/cut_size) for i in range(int(img_height/cut_size))]

    for i in range(int(img_height/cut_size)):
        for j in range(int(img_width/cut_size)):
            y = i * cut_size
            x = j * cut_size
            predict_color = ilib.color_checker(shima_region_img[y:y+cut_size, x:x+cut_size], i, j, cut_size, 'predict')

            if predict_color == 0:
                shima_count += 1
                angle = ld.estimate_angle(kessyou_img[y:y+cut_size, x:x+cut_size])
                for k in range(len(angles)):
                    if k * 10 <= angle < (k + 1) * 10:
                        angles[k] += 1
                        angle_positions[i][j] += k
                        break

    result_img = copy.deepcopy(shima_region_img)
    
    for i in range(int(img_height/cut_size)):
        for j in range(int(img_width/cut_size)):
            y = i * cut_size
            x = j * cut_size
            pt1 = (x, y)
            pt2 = (x+cut_size, y+cut_size)
            if angle_positions[i][j] > 0:
                cv2.rectangle(result_img, pt1, pt2, color[angle_positions[i][j]], cv2.FILLED)
            else:
                cv2.rectangle(result_img, pt1, pt2, (0, 0, 0), cv2.FILLED)

    print(f'shima: {shima_count}')
    for i in range(len(angles)):
        print(f'degree:{i * 10}~{(i + 1) * 10} => {angles[i]}')

    cv2.imwrite('./img/angles.jpg', result_img)

    labels = ['0~10', '10~20', '20~30', '30~40', '40~50', '50~60', '60~70', '70~80', '80~90', '90~100', '100~110', '110~120', '120~130', '130~140', '140~150', '150~160', '160~170', '170~180']
    plt.figure(figsize=(8, 6))
    plt.bar(labels, angles)
    plt.tick_params(labelsize=5.5)
    plt.xlabel('angles')
    plt.ylabel('frequency')
    plt.savefig('./img/hist.png')
    plt.clf()