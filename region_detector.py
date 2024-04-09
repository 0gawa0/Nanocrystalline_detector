import cv2
import warnings
import tensorflow.compat.v1 as tf
from tensorflow.keras.preprocessing import image
from .model import predict_class as my_class

warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=UserWarning)

config = tf.ConfigProto()
config.gpu_options.per_process_gpu_memory_fraction = 0.4  #40%
config.gpu_options.allow_growth = True
session = tf.Session(config=config)
tf.keras.backend.set_session(session)

classes = [
           'shima', 'shimanashi','taisyougai'
           ]

if __name__ == '__main__':
    # ファイルパスの設定
    filepath = './img/5120.tif'
    paramfilepath = './parameter/kessyou/kessyou_parameter'

    # 左から縞模様、縞なし、対象外の領域を塗りつぶす用の色定義
    color = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]

    # 画像の分割サイズ（学習データの画像サイズと統一する必要がある）
    cut_size = 32
    # それぞれの領域のカウント記録用配列。添字の小さい方から縞模様、縞なし、対象外について記録する
    cnt = [0, 0, 0]

    img = image.load_img(filepath)
    img = image.img_to_array(img)
    height, width = img.shape[:2]
    annotated_img = img.copy()

    print(img.shape)

    region_list = [[-1] * int(width/cut_size) for i in range(int(height/cut_size))]
    print(f'row:{len(region_list)}, col:{len(region_list[0])}')

    print('width:' + str(width))
    print('height:' + str(height))

    model = my_class.Model(paramfilepath)

    k = 1
    for i in range(int(height/cut_size)):
        for j in range(int(width/cut_size)):
            y = i * cut_size
            x = j * cut_size
            pt1 = (x, y)
            pt2 = (x+cut_size, y+cut_size)
            timg = img[y:y+cut_size, x:x+cut_size]
            resize_timg = cv2.resize(timg, (224, 224), interpolation=cv2.INTER_NEAREST)
            x = model.convert_vec(resize_timg)
            
            result = model.predict(x)
            print(f'class:{classes[result]}, count:{k}/{int(height/cut_size)*int(width/cut_size)}')
            cnt[result] += 1
            region_list[i][j] = result
            cv2.rectangle(annotated_img, pt1, pt2, color[result], cv2.FILLED)
            k += 1

    # 元画像と検出した領域を重ね合わせる
    combine_img = cv2.addWeighted(annotated_img, 0.3, img, 0.7, 0)
    cv2.imwrite('./img/kessyou_region.jpg', annotated_img)
    cv2.imwrite('./img/kessyou_result.jpg', combine_img)

    # それぞれのクラスのカウント数を表示する
    for i in range(3):
        print(f'label{i}: {cnt[i]}')