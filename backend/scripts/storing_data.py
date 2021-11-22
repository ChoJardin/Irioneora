import csv
import requests
import bs4

from artifacts.models import Artifact
from artifacts.serializers import ArtifactSerializer


# Django extensions runscript
def run():
    # 소장품 상세정보 불러오기
    URL = 'http://www.emuseum.go.kr/openapi/relic/detail'
    API_KEY = ['SrLLfGdZjGbS5OmPmSlewYvcR6tXPmpk11SduYlvFr7r6CA7L9vjF7JRSx7rhrTEvOdAlUDtqkY9HJAg8+Y6ww==',
               ]

    for key in API_KEY:
        # print(key)
        with open('scripts/국립중앙박물관_전국 박물관 유물정보_20190920..csv', encoding='cp949') as f:
            data = csv.reader(f)
            for line in data:
                if line[5] == '종교신앙':
                    # print(line)
                    id = line[0]
                    if not Artifact.objects.all().filter(identification_number=id):
                        params = {'serviceKey': key, 'id': id}

                        r = requests.get(URL, params=params)
                        # print(r.url)

                        xml_data = bs4.BeautifulSoup(r.content, 'html.parser')
                        # print(xml_data)

                        # 404
                        if xml_data.find('div', class_='error_info'):
                            # print('404')
                            continue

                        if xml_data.find('totalcount').text == '0':

                            if 'EXCEEDS' in xml_data.find('resultmsg').text:
                                # print('exceeds')
                                break

                            continue

                        image_uri = ''
                        for item in xml_data.findAll('item'):
                            if item['key'] == 'imgUri':
                                image_uri = item['value']

                        if not image_uri:
                            continue

                        data = {
                            'identification_number': id,
                            'image_uri': image_uri
                        }

                        if Artifact.objects.all().filter(image_uri=image_uri):
                            continue

                        # print()
                        # print(data)
                        # print(len(image_uri))

                        serializer = ArtifactSerializer(data=data)

                        if serializer.is_valid(raise_exception=True):
                            serializer.save()
