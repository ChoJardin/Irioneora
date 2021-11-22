from .models import RecommendedArtifact
from .serializers import RecommendedArtifactSerialize
from rest_framework.decorators import api_view 
from rest_framework.response import Response
from datetime import datetime
import requests, bs4

# constant value
service_key = "DLuSbLjmCJIDKmhoSB7ELx3eVXXxg9ZBqh9oC8/eFWTcq2gDMqfQA7jrooSkvzWgYv/pd9a6fUJKG40K3VQXHg=="

@api_view(['GET'])
def artifact_save_recommend(request,pageNo):
    
    # 1. 페이지 선정 및 페이지 내 모든 유물 정보 가져오기
    artifact_url = f"http://www.emuseum.go.kr/openapi/relic/list?serviceKey={service_key}&numOfRows=100&pageNo={pageNo}"
    #http://www.emuseum.go.kr/openapi/relic/list?serviceKey=DLuSbLjmCJIDKmhoSB7ELx3eVXXxg9ZBqh9oC8/eFWTcq2gDMqfQA7jrooSkvzWgYv/pd9a6fUJKG40K3VQXHg==&numOfRows=100&pageNo=1

    response = requests.get(artifact_url)
    response_dict = bs4.BeautifulSoup(response.content, 'html.parser')
    search_list = []

    for data in response_dict.findAll('data'):
        for item in data.findAll('item'):
            if item['key'] == 'id':
                id_num = item['value']
        search_list.append(id_num)

    # 2-1. 변수설정
    detail_list = []
    dataDict = {
        'id_num': '',
        'name': '',
        'desc': '',
        'museum_name': '',
        'nationality_name': '',
        'image_uri': '',
    }

    # 2-2. 모든 유물에서 desc있나 파악하기
    for i in range(len(search_list)):
        artifact_num = search_list[i]
        artifact_url = f"http://www.emuseum.go.kr/openapi/relic/detail?serviceKey={service_key}&id={artifact_num}"
        # http://www.emuseum.go.kr/openapi/relic/detail?serviceKey=DLuSbLjmCJIDKmhoSB7ELx3eVXXxg9ZBqh9oC8/eFWTcq2gDMqfQA7jrooSkvzWgYv/pd9a6fUJKG40K3VQXHg==&id=PS0100100100100021500000
        
        response = requests.get(artifact_url)
        response_dict = bs4.BeautifulSoup(response.content, 'html.parser')

        for data in response_dict.findAll('list'):
            for item in data.findAll('item'):
                if item['key'] == 'id':
                    dataDict['id_num'] = item['value']

                elif item['key'] == 'desc':
                    dataDict['desc'] = item['value']

                elif item['key'] == 'nameKr':
                    dataDict['name'] = item['value']

                elif item['key'] == 'nationalityName2':
                    dataDict['nationality_name'] = item['value']

                elif item['key'] == 'museumName2':
                    dataDict['museum_name'] = item['value']

                elif item['key'] == 'imgThumUriM':
                    dataDict['image_uri'] = item['value']

            # 2-3 db에 저장하기
            if dataDict['desc'] != '':
                serializer = RecommendedArtifactSerialize(data=dataDict)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                dataDict = {
                    'id_num': '',
                    'name': '',
                    'desc': '',
                    'museum_name': '',
                    'nationality_name': '',
                    'image_uri': '',
                }   
    return Response(serializer.data)


@api_view(['GET'])
def artifact_recommend(request):
    ## 오늘은 며칠째인가요??
    now  = datetime.now()
    nowYear = now.year
    nowMonth = now.month
    nowDay = now.day
    daySum = 0

    if nowYear%4==0 and nowYear%100!=0 or nowYear%400==0:
        month = [31,29,31,30,31,30,31,31,30,31,30,31]
    else:
        month = [31,28,31,30,31,30,31,31,30,31,30,31]
    
    for i in range(nowMonth-1):
        daySum += month[i]

    daySum += nowDay

    Recommended_list = RecommendedArtifact.objects.all()
    Recommended_artifact =  Recommended_list[daySum]
    dataDict = {
                    'id_num': Recommended_artifact.id_num,
                    'name': Recommended_artifact.name,
                    'desc': Recommended_artifact.desc,
                    'museum_name': Recommended_artifact.museum_name,
                    'nationality_name': Recommended_artifact.nationality_name,
                    'image_uri': Recommended_artifact.image_uri,
                }   
    # print(Recommended_artifact.name)

    return Response(dataDict)
