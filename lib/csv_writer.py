import numpy as np
import json

# このファイル内にある関数群は無視して構いません

def write_for_json(data, fileName):
    a = None
    if type(data) is np.ndarray:
        a = data.tolist()
    elif type(data) is list:
        a = data
    
    with open(fileName, 'w') as f:
        f.write(json.dumps(a, indent=2))
        print('write')

def add_for_json(data, row, col, img_name, fileName):
    a = None
    if type(data) is np.ndarray:
        a = data.tolist()
    elif type(data) is list:
        a = data

    result = {
                "name":img_name,
                "row":row,
                "col":col,
                "data":a
            }
    
    with open(fileName, 'a') as f:
        f.write(json.dumps(result, indent=2) + '\n')