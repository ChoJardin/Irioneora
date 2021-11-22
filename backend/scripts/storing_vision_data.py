# 유물 사진 URL을 넣어서 vision API에 적용해보자!
# CSV 파일로 만들 것!


# day1은 4000 row까지 긁었음

from get_vision_data import *
import pymysql
import json

host = "j5a601.p.ssafy.io"
user = "irioneora"
pw = "dlfldhsjfk"
db = "irioneora"

conn = pymysql.connect( host= host, user = user, password = pw, db = db)

sql = "select * from artifacts_artifact where id > 7000 limit 1000;"

# 쿼리 실행
curs = conn.cursor()
curs.execute(sql)

uris = curs.fetchall()

# today's result
result = []

for i in range(len(uris)):

    identification_number = uris[i][1]
    image_uri = uris[i][2]

    # print(i)
    # print(identification_number)
    # print(image_uri)

    data = get_vision_data(image_uri)

    try:
        if len(data["result"]["faces"]) == 0:
            continue
        else:
            # print(f'i have face. idx{i}')
            result.append({identification_number: data})
    except:
        continue

# json_string = json.dumps(result)


with open('16000to20000.json', 'w') as f:
    json.dump(result, f)


# print("Today end!")
# print(len(result))