from django.shortcuts import get_object_or_404

from artifacts.models import Artifact
# from artifacts.serializers import ArtifactResembleSerializer


from rest_framework.decorators import api_view
from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated


import numpy as np
import pandas as pd

import pyspark.sql.functions as F
from pyspark.sql import SparkSession, SQLContext
from pyspark.sql.types import DoubleType

from pyspark.ml.feature import VectorAssembler
from pyspark.ml.feature import PCA
from pyspark.ml.feature import PCAModel

from scipy.spatial import distance


# 인풋된 유저 얼굴 데이터 변환
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

    for k, v in face['facial_points'].items():
        data.update(get_polygon_info(k, v))

def decode_one_image(o):
    ret = []

    rid = o['rid']
    r = o['result']

    width = r['width']
    height = r['height']

    for face in r['faces']:
        data = decode_face(face)
        data.update({'identification': 'User', 'rid': rid, 'width': width, 'height': height})
        ret.append(data)

    return ret

# 유저 얼굴 데이터 받아와서 닮은 얼굴 뿌리기
@api_view(['POST'])
def user_face(request):
    try:
        spark = SparkSession\
                .builder\
                .master('spark://j5a601.p.ssafy.io:7077')\
                .appName('Search')\
                .getOrCreate()

    except:
        pass

    # print(request.data)

    ret = [ decode_one_image(request.data)[0] ]
    # print(ret)

    ret_df =  pd.DataFrame(ret)
    # print(ret_df)

    userDf = spark.createDataFrame(ret_df)
    # print(userDf)
    
    training_vectorize = VectorAssembler(
        inputCols=[
            # 'age',  
            'gender',
            # 'x','y','w','h','yaw','pitch','roll',
            # 'score',
            'left_eyebrow_x_mean','left_eyebrow_y_mean','left_eyebrow_x_min','left_eyebrow_x_max','left_eyebrow_y_min','left_eyebrow_y_max',
            'jaw_x_mean','jaw_y_mean','jaw_x_min','jaw_x_max','jaw_y_min','jaw_y_max',
            'left_eye_x_mean','left_eye_y_mean','left_eye_x_min','left_eye_x_max','left_eye_y_min','left_eye_y_max',
            'lip_x_mean','lip_y_mean','lip_x_min','lip_x_max','lip_y_min','lip_y_max',
            'nose_x_mean','nose_y_mean','nose_x_min','nose_x_max','nose_y_min','nose_y_max',
            'right_eye_x_mean','right_eye_y_mean','right_eye_x_min','right_eye_x_max','right_eye_y_min','right_eye_y_max',
            'right_eyebrow_x_mean','right_eyebrow_y_mean','right_eyebrow_x_min','right_eyebrow_x_max','right_eyebrow_y_min','right_eyebrow_y_max',
            # identification,rid,width,height
        ],
        outputCol='features'
    )


    userData = training_vectorize.transform(userDf)
    # print('----------- load model')
    model = PCAModel.load('hdfs://j5a601.p.ssafy.io:9000/models/2')
    # print('----------- load done')
    # print(model.pc)
    # print(model)
    # print(userData)

    # adjust model
    sc = spark.sparkContext
    sqlContext = SQLContext(sc)
    dataset = sqlContext.read.format('parquet').load('hdfs://j5a601.p.ssafy.io:9000/data')
    # print('------------- dataset')
    # print(dataset)
    processed = model.transform(dataset)
    user = model.transform(userData)
    check_point = user.collect()[0].output

    distance_udf = F.udf(lambda x: float(distance.euclidean(x, check_point)), DoubleType())
    top5 = processed.withColumn('distances', distance_udf(F.col('output'))).orderBy('distances').take(5)

    # print('------------- result')
    # print(top5)

    resultData = []
    for sel in top5:
        resultData.append({'identification': sel['identification'], 'width': sel['width'], 'height': sel['height'], 'x': sel['x'], 'y': sel['y'], 'w': sel['w'], 'h': sel['h']})
    # print(resultData)

    dummydata = [
        {'identification': 'PS0100100102102727900000', 'name': '이건첫번째야', 'width': 3000, 'height': 2000, 'x': 0.4754312744140625, 'y': 0.6482667846679687, 'w': 0.05687882486979168, 'h': 0.08531817626953131},
        {'identification': 'PS0100100100900173100000', 'name': '이건두번째고', 'width': 669, 'height': 515, 'x': 0.43930195122734494, 'y': 0.11844135765890473, 'w': 0.08157868663291756, 'h': 0.10597306038569479},
        # 같은 그림에 두 얼굴
        {'identification': 'PS0100100100900260500000', 'name': '아이스크림이', 'width': 1592, 'height': 3000, 'x': 0.6141179913851484, 'y': 0.5116527506510417, 'w': 0.08356299472214579, 'h': 0.044344075520833304},        
        {'identification': 'PS0100100100900260500000', 'name': '먹고싶어', 'width': 1592, 'height': 3000, 'x': 0.3875239003243758, 'y': 0.6396309000651041, 'w': 0.06894641665358042, 'h': 0.036587605794270894},
    ]

    for i in range(len(resultData)):
        artifact_id = resultData[i]['identification']
        artifact = get_object_or_404(Artifact, identification_number=artifact_id)
        # print(artifact.image_uri)
        resultData[i]['url'] = artifact.image_uri
        resultData[i]['name'] = artifact.artifact_name


    # 닮은 유물 저장
    # print('-----------')
    # print(request.user.is_authenticated)
    user = request.user
    if user.is_authenticated:
        artifact = get_object_or_404(Artifact, identification_number=resultData[0]['identification'])
        # print(artifact)
        if artifact.resemble_users.filter(username=user).exists():
            pass
        
        else:
            artifact.resemble_users.add(user)

    return Response(resultData)
    # return HttpResponse(200)
