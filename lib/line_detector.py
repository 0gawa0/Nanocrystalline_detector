import numpy as np
import cv2
import math
from pylsd.lsd import lsd

def estimate_angle(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    lines = lsd(gray)
    angles_list = []

    for i in range(lines.shape[0]):
        tan = (lines[i, 1]-lines[i, 3])/(lines[i, 0]-lines[i, 2])

        '''
        atan:-90~90度（ラジアン）の範囲の角度を返す
        下記のプログラムでは0~180度を返すように調整している
        （atanが負であれば角度は90より大きくなる）
        '''
        if tan < 0:
            deg = 180 + math.degrees(math.atan(tan))
        else:
            deg = math.degrees(math.atan(tan))

        angles_list.append(deg)
    
    print(f'find lines:{angles_list}')
    avg_angle = np.mean(angles_list)
    
    return avg_angle
