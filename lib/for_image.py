import numpy as np
import sys
from .csv_writer import add_for_json

direction = [[-1, -1], [0, -1], [1, -1], [-1, 0], [1, 0], [-1, 1], [0, 1], [1, 1]]

# B、R、Gのいずれでもない場合を判定する関数
def color_count_checker(count_list: list):
    if len(count_list) != 3:
        print("Error: list size is not 3.", file=sys.stderr)
        sys.exit(1)
    
    return count_list[0] == -1 and count_list[1] == -1 and count_list[2] == -1

# 読み込んだ32×32サイズの領域がどの色で塗りつぶされているかをチェックする関数
def color_checker(cut_region, row, col, cut_size, img_name,):
    color_count = [-1, -1, -1]
    if type(cut_region) is np.ndarray:
        for i in range(cut_size):
            for j in range(cut_size):
                for k in range(3):
                    if cut_region[i][j][k] >= 245:
                        if color_count[k] == -1:
                            color_count[k] = 0
                        color_count[k] += 1

    # デバッグ用（色の判定時に意図した色の領域を認識しているかをチェックする）
    if np.max(color_count) < 900 and not(color_count_checker(color_count)):
        print(f'img:{img_name}, row:{row}, col:{col}')
        print(f'color: {color_count}, max:{np.max(color_count)}, index:{np.argmax(color_count)}')
        add_for_json(color_count, row, col, img_name, './csv/kensyou_output.json')
    # デバッグ用プログラムはここまで
    
    if color_count[0] == -1 and color_count_checker(color_count):
        return -1
    
    if np.max(color_count) >= 900:
        return np.argmax(color_count)
    else:
        return -1

def isDistance(a, b, e):
    return abs(a - b) > e

# グレースケールかどうかを判定する
def isColor(cut_region, cut_size):
    if type(cut_region) is np.ndarray:
        for i in range(cut_size):
            for j in range(cut_size):
                B = cut_region[i][j][0]
                G = cut_region[i][j][1]
                R = cut_region[i][j][2]
                if isDistance(B, G, 150) or isDistance(G, R, 150) or isDistance(R, B, 150):
                    return True
        
        return False

# 独立したマスを塗りつすための関数
def remove_one_dot(dataList: list):
    row = len(dataList)
    col = len(dataList[0])

    for i in range(1, row-1):
        for j in range(1, col-1):
            color = [-1, -1, -1]
            attention_color = dataList[i][j]
            for move in direction:
                if color[dataList[i+move[0]][j+move[1]]] == -1:
                    color[dataList[i+move[0]][j+move[1]]] = 0
                color[dataList[i+move[0]][j+move[1]]] += 1
            
            most_appearance_color_index = np.argmax(color)
            if most_appearance_color_index != attention_color and np.max(color) > 5:
                dataList[i][j] = most_appearance_color_index
    
    result = dataList
    return result