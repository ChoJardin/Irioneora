# make features vector 

from pyspark.ml.feature import VectorAssembler
from pyspark.ml.feature import PCA
from pyspark.ml.feature import PCAModel
from pyspark.sql import SparkSession
import pandas as pd 


spark = SparkSession.builder.master('spark://j5a601.p.ssafy.io:7077').appName('test').getOrCreate()

# df = spark.read.option("inferSchema",True).csv('data.csv', header=True)

# hdfs dfs -copyFromLocal ./data.csv /rawdata/data.csv
df = spark.read.option("inferSchema",True).csv('hdfs://127.0.0.1:9000/rawdata/data.csv', header=True)


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
dataset = training_vectorize.transform(df)
dataset.write.save('hdfs://127.0.0.1:9000/data', format='parquet')

# print(dataset)


# PCA Dimensionality Reduction

def make_model(k):
    pca = PCA(k=k, inputCol='features', outputCol='pca_features')
    model = pca.fit(dataset)
    model.setOutputCol('output')
    print( f'K = {k} : {model.explainedVariance}')
    model.save(f'hdfs://127.0.0.1:9000/models/{k}')
#print(model.transform(dataset).collect()[0].output)

for k in range(2,7):
    make_model(k)

#model2 = PCAModel.load('test_model')
#print(model2.transform(dataset).collect()[0].output)