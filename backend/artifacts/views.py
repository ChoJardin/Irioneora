from os import error
from django.http.response import HttpResponse
from django.shortcuts import render, get_object_or_404
from rest_framework import serializers
from rest_framework.serializers import Serializer
from rest_framework.views import APIView

from .models import Artifact
from .serializers import ArtifactSerializer, ArtifactLikeSerializer, ArtifactResembleSerializer, ArtifactDetailSerializer

from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


import csv
import requests
import bs4


from konlpy.tag import Okt, Kkma, Twitter
from collections import Counter

# API_KEY
API_KEY = 'SrLLfGdZjGbS5OmPmSlewYvcR6tXPmpk11SduYlvFr7r6CA7L9vjF7JRSx7rhrTEvOdAlUDtqkY9HJAg8+Y6ww=='

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

    with open('./국립중앙박물관_전국 박물관 유물정보_20190920..csv', encoding='cp949') as f:
        data = csv.reader(f)
        for line in data:
            if line[5] == '문화예술' or line[5] == '종교신앙':
                id = line[0]
                if not Artifact.objects.all().filter(identification_number=id):
                    params = {'serviceKey': API_KEY, 'id': id}

                    r = requests.get(URL, params=params)

                    xml_data = bs4.BeautifulSoup(r.content, 'html.parser')

                    # print(xml_data)
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


# 유물 상세정보
@api_view(['GET'])
def artifact_detail(request, artifact_id):
    
    artifact_url = f'http://www.emuseum.go.kr/openapi/relic/detail'
    params = {'serviceKey': API_KEY, 'id': artifact_id}
    
    raw_data = requests.get(artifact_url, params=params)
    pretty_data = bs4.BeautifulSoup(raw_data.content, 'html.parser')    

    # 초기화 설정 해주지 않으면
    # UnboundLocalError: local variable 'desc' referenced before assignment 에러를 마주하게 된다.
    data = {
        'identification_number': artifact_id,
        'artifact_name': '이름 정보가 없습니다.',
        'artifact_size': '크기 정보가 없습니다.',
        'artifact_author': '작가 정보가 없습니다.',
        'description': '상세 정보가 없습니다.',
        'museum_name': '박물관 정보가 없습니다.',
        'index_words': '색인어 정보가 없습니다.',
        'nationality_name': '시대 정보가 없습니다.',
        'image_uri': '',
    }

    # 반복문 순회하며 해당 item의 key값에 따라 덮어씌우기
    for item in pretty_data.find_all('item'):
        if item.get('key') == "name":
            data['artifact_name'] = item.get('value')
        
        if item.get('key') == "sizeInfo":
            data['artifact_size'] = item.get('value')
        
        if item.get('key') == "author":
            data['artifact_author'] = item.get('value')
        
        if item.get('key') == "desc":
            data['description'] = item.get('value')
        
        if item.get('key') == "museumName2":
            data['museum_name'] = item.get('value')

        if item.get('key') == "indexWord":
            data['index_words'] = item.get('value')

        if item.get('key') == "nationalityName2":    
            data['nationality_name'] = item.get('value')

        if item.get('key') == "imgUri":
            data['image_uri'] = item.get('value')
        
    # artifact uri 수정
    split_artifact_img = list(data['image_uri'].partition('/'))

    for i in range(1, len(split_artifact_img)):
        artifact_img_uri = 'www.emuseum.go.kr/' + split_artifact_img[i]

    data['image_uri'] = artifact_img_uri

    # decription 내 html 엔티티 삭제
    # &prime; 과 같은 문자열 삭제하기
    problem_idx = []
    for i in range(len(data['description'])):
        if data['description'][i] == '&':
            idx = 0
            while data['description'][i+idx] != ';':
                problem_idx.append(i+idx)
                idx += 1
            problem_idx.append(i+idx)
    
    list_description = list(data['description'])
    for j in range(len(problem_idx)):
        list_description[problem_idx[j]] = ''
    
    str_description = ''
    for k in range(len(list_description)):
        str_description += list_description[k]

    data['description'] = str_description

    # serializer로 data response
    serializer = ArtifactDetailSerializer(data=data)
    if serializer.is_valid(raise_exception=True):
        return Response(serializer.data)
    else:
        error_data = {'message': 'error'}
        return Response(error_data)

# 워드 클라우드
@api_view(['GET'])
def wordcloud(request, artifact_id):
    # 해당 유물에 대한 정보 받아오기
    artifact_url = f'http://www.emuseum.go.kr/openapi/relic/detail'
    params = {'serviceKey': API_KEY, 'id': artifact_id}

    raw_data = requests.get(artifact_url, params=params)
    pretty_data = bs4.BeautifulSoup(raw_data.content, 'html.parser')

    ori_description = ''
    ori_indexWords = ''
    ori_nationality_1 = ''
    ori_nationality_2 = ''
    ori_materialName = ''
    ori_purposeName1 = ''
    ori_purposeName2 = ''
    ori_purposeName3 = ''
    ori_purposeName4 = ''
    relt_id = ''

    for item in pretty_data.find_all('item'):
        if item.get('key') == "desc":
            ori_description = item.get('value')

        if item.get('key') == "indexWord":
            ori_indexWords = item.get('value')

        if item.get('key') == "nationalityName1":
            ori_nationality_1 = item.get('value')

        if item.get('key') == "nationalityName2":
            ori_nationality_2 = item.get('value')

        if item.get('key') == "materialName1":
            ori_materialName = item.get('value')

        if item.get('key') == "purposeName1":
            ori_purposeName1 = item.get('value')

        if item.get('key') == "purposeName2":
            ori_purposeName2 = item.get('value')

        if item.get('key') == "purposeName3":
            ori_purposeName3 = item.get('value')

        if item.get('key') == "purposeName4":
            ori_purposeName4 = item.get('value')

        if item.get('key') == "reltId":
            relt_id = item.get('value')

    # 관련 유물에 대한 정보 받아오기
    if relt_id:
        artifact_url = f'http://www.emuseum.go.kr/openapi/relic/detail'
        params = {'serviceKey': API_KEY, 'id': relt_id}

        raw_data = requests.get(artifact_url, params=params)
        pretty_data = bs4.BeautifulSoup(raw_data.content, 'html.parser')

        rel_description = ''
        rel_indexWords = ''
        rel_nationality_1 = ''
        rel_nationality_2 = ''
        rel_materialName = ''
        rel_purposeName1 = ''
        rel_purposeName2 = ''
        rel_purposeName3 = ''
        rel_purposeName4 = ''

        for item in pretty_data.find_all('item'):
            if item.get('key') == "desc":
                rel_description = item.get('value')

            if item.get('key') == "indexWord":
                rel_indexWords = item.get('value')

            if item.get('key') == "nationalityName1":
                rel_nationality_1 = item.get('value')

            if item.get('key') == "nationalityName2":
                rel_nationality_2 = item.get('value')

            if item.get('key') == 'materialName1':
                rel_materialName = item.get('value')

            if item.get('key') == "purposeName1":
                rel_purposeName1 = item.get('value')

            if item.get('key') == "purposeName2":
                rel_purposeName2 = item.get('value')

            if item.get('key') == "purposeName3":
                rel_purposeName3 = item.get('value')

            if item.get('key') == "purposeName4":
                rel_purposeName4 = item.get('value')

        ori_info = ori_description + ori_indexWords + ori_nationality_1 + ori_nationality_2 + ori_materialName + ori_purposeName1 + ori_purposeName2 + ori_purposeName3 + ori_purposeName4
        rel_info = rel_description + rel_indexWords + rel_nationality_1 + rel_nationality_2 + rel_materialName + rel_purposeName1 + rel_purposeName2 + rel_purposeName3 + rel_purposeName4
        sentences = ori_info + rel_info

    sentences = ori_description + ori_indexWords + ori_nationality_1 + ori_nationality_2 + ori_materialName + ori_purposeName1 + ori_purposeName2 + ori_purposeName3 + ori_purposeName4

    okt = Okt()
    count = Counter()

    # 형태소 구분
    morpheme = okt.pos(sentences)

    # 명사, 형용사 선별
    noun_and_adj = []
    for word, tag in morpheme:
        if tag in ['Noun', 'Adjective']:
            noun_and_adj.append(word)

    # 빈도수와 함께 출력
    count = Counter(noun_and_adj)
    common_50 = count.most_common(50)  # 상위 50개 출력

    # key - name, value - 빈도수 형태의 딕셔너리로 변환
    # [{'name': '병풍', 'value': 5}, {'name': '의궤', 'value': 4}, {'name': '폭', 'value': 4} .. 이하 생략
    result = []
    for i in range(len(common_50)):
        nv_dict = {'name': common_50[i][0], 'value': common_50[i][1]}
        result.append(nv_dict)
    # print(result)

    return Response(result)

# 유물 좋아요
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def artifact_like(request, artifact_id):
    user = request.user
    # print(user)

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

    # print('-----------------------------', artifact.like_users.all())
    serializer = ArtifactLikeSerializer(artifact)
    return Response(serializer.data)

# 닮은 유물 저장
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def artifact_resemble(request, artifact_id):
    artifact = get_object_or_404(Artifact, identification_number=artifact_id)
    user = request.user

    if artifact.resemble_users.filter(username=user).exists():
        pass
    
    else:
        artifact.resemble_users.add(user)
    
    serializer = ArtifactResembleSerializer(artifact)
    return Response(serializer.data)

# 박물관 정보
@api_view(['GET'])
def get_museum_info(request, museum_name):
    museum_url = f'http://api.data.go.kr/openapi/tn_pubr_public_museum_artgr_info_api'
    API_KEY = 'SqZskQNLBydKAJrTV5fUn3zRuenH7ELym5KvJWma15ABpxIYBeQK15yeq+cLDfiGBiMv8Pt5VFk1H0Sz4lX3yw=='
    params = {'serviceKey': API_KEY, 'fcltyNm': museum_name}

    raw_data = requests.get(museum_url, params=params)
    pretty_data = bs4.BeautifulSoup(raw_data.content, 'html.parser')    
    
    data = {
        'fclty_name': '',
        'fclty_type': '',
        'address': '',
        'homepage': '',
        'weekday_open': '',
        'weekday_close': '',
        'holiday_open': '',
        'holiday_close': '',
        'closed_date': '',
        'adult_chrg': '',
        'student_chrg': '',
        'child_chrg': '',
        'introduction': '',
    }

    data['fclty_name'] = pretty_data.find('fcltynm').text
    data['fclty_type'] = pretty_data.find('fcltytype').text
    data['address'] = pretty_data.find('rdnmadr').text
    data['homepage'] = pretty_data.find('homepageurl').text
    data['weekday_open'] = pretty_data.find('weekdayoperopenhhmm').text
    data['weekday_close'] = pretty_data.find('weekdayopercolsehhmm').text
    data['holiday_open'] = pretty_data.find('holidayoperopenhhmm').text
    data['holiday_close'] = pretty_data.find('holidaycloseopenhhmm').text
    data['closed_date'] = pretty_data.find('rstdeinfo').text
    data['adult_chrg'] = pretty_data.find('adultchrge').text
    data['student_chrg'] = pretty_data.find('yngbgschrge').text
    data['child_chrg'] = pretty_data.find('childchrge').text
    data['introduction'] = pretty_data.find('fcltyintrcn').text

    return Response(data)

