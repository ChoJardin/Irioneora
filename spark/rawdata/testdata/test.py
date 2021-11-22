import json
import math
import numpy as np

FACE_KEYS = ['left_eyebrow', 'right_eyebrow', 'left_eye','right_eye', 'nose', 'lip', 'jaw' ]

def get_faces_from_kakao_response(res):
    if 'result' not in res:
        return []
    if 'faces' not in res['result']:
        return []
    return res['result']['faces']

def get_feature(polygon):
    def get_triangle_area(a,b,c):
        return abs( a[0]*b[1] + b[0]*c[1] + c[0]*a[1] - a[1]*b[0] - b[1]*c[0] - c[1]*a[0]) / 2

    x = 0
    y = 0
    cnt = len(polygon)
    for pos in polygon:
        x += pos[0]
        y += pos[1]
    center = [ x / cnt, y / cnt ]

    area = 0
    before = polygon[-1]
    for pos in polygon:
        area += get_triangle_area(before, pos, center)
    return center + [area]

def get_features(face):
    ret = []
    for key in FACE_KEYS:
        ret.append( get_feature(face['facial_points'][key]))
    
    return ret

def get_distance( face_a, face_b):
    features_a = get_features(face_a)
    features_b = get_features(face_b)    

    dis = 0
    for i in range(len(FACE_KEYS)):
        x = features_a[i][0] - features_b[i][0]
        y = features_a[i][1] - features_b[i][1]
        area = features_a[i][2] - features_b[i][2]
        dis += math.sqrt( x*x + y*y + area*area )
        #dis += math.sqrt( x*x + y*y)
    
    return dis

with open('sample.json', 'r') as f:
    sample_faces = get_faces_from_kakao_response(json.load(f))

#print(sample_faces)
sample = sample_faces[0]

def test(fn):
    with open(fn,'r') as f:
        data = json.load(f)
        dist_dict = {}
        for entry in data:
            for k, v in entry.items():
                faces = get_faces_from_kakao_response(v)
                for i in range(len(faces)):
                    dis = get_distance(sample, faces[i])
                    if dis > 0:
                        dist_dict[ dis ] = (k,i)
        arr = np.array(list(dist_dict.keys()))
        print( f'mean: {np.mean(arr)}, min:{np.min(arr)}, max:{np.max(arr)}, std:{np.std(arr)}')
        print(dist_dict[np.min(arr)])
        print(min(arr))


test('test_faces.json')
test('test_faces_suji.json')
test('test_faces_soonjae.json')