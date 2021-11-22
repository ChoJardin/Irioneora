# Pyspark DataFrame에 맞게

import json, os, glob
import numpy as np
import pandas as pd


def get_polygon_info(prefix, polygon):
    x = [p[0] for p in polygon]
    y = [p[1] for p in polygon]

    return {
        f'{prefix}_x_mean': np.average(x),
        f'{prefix}_y_mean': np.average(y),
        f'{prefix}_x_min': np.min(x),
        f'{prefix}_x_max': np.max(x),
        f'{prefix}_y_min': np.min(y),
        f'{prefix}_y_max': np.max(y),
    }


def decode_face(face):
    keys = ['x', 'y', 'w', 'h', 'yaw', 'pitch', 'roll', 'score']
    data = dict()
    data['age'] = face['facial_attributes']['age']
    data['gender'] = face['facial_attributes']['gender']['female']

    data.update({k: face[k] for k in keys})

    for k, v in face['facial_points'].items():
        data.update(get_polygon_info(k, v))

    return data


def decode_one_image(o):
    ret = []
    for key, v in o.items():
        rid = v['rid']
        r = v['result']

        width = r['width']
        height = r['height']

        for face in r['faces']:
            data = decode_face(face)
            data.update({'identification': key, 'rid': rid, 'width': width, 'height': height})
            ret.append(data)

    return ret


# def run(filename):
#     ret = []
#     with open(filename, 'r') as f:
#         for obj in json.load(f):
#             ret.extend(decode_one_image(obj))
#     df = pd.DataFrame(ret)
#     df.to_csv(os.path.splitext(filename)[0] + '.csv')


# Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     for fn in glob.glob(os.path.join(os.getcwd(), '*.json')):
#         print(fn)
#         run(fn)


files = [
    '1to4000.json', '4000.json', '5000.json', '6000.json', '7000.json',
    '8000to12000.json', '12000to16000.json', '16000to20000.json', '20000to21000.json',
]

rawdata = []

for file in files:
    ret = []
    with open(file, 'r') as jason_file:
        jason_to_python = json.load(jason_file)
        for obj in jason_to_python:
            ret.extend(decode_one_image(obj))
    
    print(file)
    rawdata.extend(ret)

df = pd.DataFrame(rawdata)
df.to_csv('rawdata.csv')