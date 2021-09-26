from django.shortcuts import render, get_object_or_404
from rest_framework.serializers import Serializer

from .models import Artifact
from .serializers import ArtifactSerializer, ArtifactLikeSerializer, ArtifactResembleSerializer

from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from urllib.request import urlopen
import json
import csv
import requests
import bs4
import xmltodict
import pprint

# 저장 여부 확인
def is_saved(id):
    if not Artifact.objects.all().filter(identification_number=id):
        return False


# db에 저장
def save_to_db(data):
    serializer = ArtifactSerializer(data=data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()


def get_csv():
    # 소장품 상세정보 불러오기
    URL = 'http://www.emuseum.go.kr/openapi/relic/detail'
    API_KEY = 'SrLLfGdZjGbS5OmPmSlewYvcR6tXPmpk11SduYlvFr7r6CA7L9vjF7JRSx7rhrTEvOdAlUDtqkY9HJAg8+Y6ww=='

    with open('./국립중앙박물관_전국 박물관 유물정보_20190920..csv', encoding='cp949') as f:
        data = csv.reader(f)
        for line in data:
            if line[5] == '문화예술' or line[5] == '종교신앙':
                id = line[0]
                if not Artifact.objects.all().filter(identification_number=id):
                    params = {'serviceKey': API_KEY, 'id': id}

                    r = requests.get(URL, params=params)

                    xml_data = bs4.BeautifulSoup(r.content, 'html.parser')

                    print(xml_data)
                    for item in xml_data.findAll('item'):
                        if item['key'] == 'imgUri':
                            image_uri = item['value']

                    data = {
                        'identification_number': id,
                        'image_uri': image_uri
                    }

                    serializer = ArtifactSerializer(data=data)

                    if serializer.is_valid(raise_exception=True):
                        serializer.save()

                    break


service_key = 'SqZskQNLBydKAJrTV5fUn3zRuenH7ELym5KvJWma15ABpxIYBeQK15yeq+cLDfiGBiMv8Pt5VFk1H0Sz4lX3yw=='

# 유물 상세정보
@api_view(['GET'])
def artifact_detail(request, artifact_id):
    
    # 유물 상세 정보 가져오기
    artifact_url = f"http://www.emuseum.go.kr/openapi/relic/detail?serviceKey={service_key}&id={artifact_id}"
    url_open = urlopen(artifact_url)
    response_xml = url_open.read().decode('utf-8')
    response_dict = xmltodict.parse(response_xml)
    response_json = json.dumps(response_dict)

    #수정 vue에 필요한 응답을 만들기
    return Response(response_json)


# 유물 좋아요
@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def artifact_like(request, artifact_id):
    user = request.user

    # 좋아요한 artifact가 DB에 없는 경우 → 저장 후 좋아요하기
    if not Artifact.objects.all().filter(identification_number = artifact_id):
        artifact_url = f'http://www.emuseum.go.kr/openapi/relic/detail'
        API_KEY = 'SqZskQNLBydKAJrTV5fUn3zRuenH7ELym5KvJWma15ABpxIYBeQK15yeq+cLDfiGBiMv8Pt5VFk1H0Sz4lX3yw=='
        params = {'serviceKey': API_KEY, 'id': artifact_id}

        raw_data = requests.get(artifact_url, params=params)
        pretty_data = bs4.BeautifulSoup(raw_data.content, 'html.parser')
        # pprint.pprint(pretty_data)

        for item in pretty_data.find_all('item'):
            if item.get('key') == "imgUri":
                artifact_img = item.get('value')

        # artifact_img 주소: '211.252.141.58/openapi/img?serviceKey=%2F%2BRIMbHtvxv0Qjz6tKz5DqXD5svR9t4DN.. 이하 생략'
        # partition을 사용 → '/'을 기준으로 문자열을 자름 → ('211.252.141.58', '/', 'openapi/img?serviceKey=7QIFITdRH1k.. 이하 생략')
        split_artifact_img = list(artifact_img.partition('/'))

        for i in range(1, len(split_artifact_img)):
            artifact_img_uri = 'www.emuseum.go.kr/' + split_artifact_img[i]
        
        artifact_data = {
            'identification_number': artifact_id,
            'image_uri': artifact_img_uri
        }

        serializer = ArtifactSerializer(data=artifact_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()


    artifact = get_object_or_404(Artifact, identification_number=artifact_id)

    if artifact.like_users.filter(username=user).exists():
        artifact.like_users.remove(user)

    else:
        artifact.like_users.add(user)

    serializer = ArtifactLikeSerializer(artifact)
    return Response(serializer.data)


# 닮은 유물 저장
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def artifact_resemble(request, artifact_pk):
    artifact = get_object_or_404(Artifact, pk=artifact_pk)
    user = request.user

    if artifact.resemble_users.filter(username=user).exists():
        pass
    
    else:
        artifact.resemble_users.add(user)
    
    serializer = ArtifactResembleSerializer(artifact)
    return Response(serializer.data)