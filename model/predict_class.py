from tensorflow.keras.models import Model
from tensorflow.keras import utils
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.vgg19 import VGG19
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg19 import preprocess_input
import tensorflow.compat.v1 as tf
import keras
import numpy as np

class Model:
    # クラスを呼び出すときはパラメータ（学習時に作成したモデル）ファイルを引数に指定しておく
    def __init__(self, param: str) -> None:
        # 入力画像をベクトルに変換するためのVGG19アーキテクチャを事前に読み込む
        self.param = param
        self.vgg_model = VGG19(weights='imagenet')
        self.pp_model = keras.Model(inputs=self.vgg_model.input, outputs=self.vgg_model.get_layer('fc2').output)
        self.pp_model.summary()

    def convert_vec(self, val_x):
        x = np.expand_dims(val_x, axis=0)
        x = preprocess_input(x)
        return self.pp_model.predict(x)

    def predict(self, val_x):
        result = np.zeros(3)

        #5分割交差検証を行っているため5個のモデルでそれぞれ精度を確認
        y_pred = []
        for i in range(5):
            i += 1
            # モデルのロード。重みやバイアスといったパラメータを読み込む
            model = load_model(self.param + str(i) + '.h5')
            y_pred.append(model.predict(val_x))
        
        for i in range(len(y_pred)):
            for j in range(len(y_pred[0][0])):
                result[j] += y_pred[i][0][j]
        
        result = result / 5

        return np.argmax(result)

