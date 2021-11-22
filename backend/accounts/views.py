from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import render, redirect, get_object_or_404
import requests

# 중복확인
from rest_framework.decorators import api_view
from django.contrib.auth import get_user_model

User = get_user_model()

# 카카오 로그인
from rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.kakao import views as kakao_views
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.socialaccount.models import SocialAccount



# 회원가입시 닉네임 중복 확인
@api_view(['GET'])
def username_duplicate_check(request):
    username = request.GET['username']
    data = {
        'error': True,
        'result': '이미 사용중인 아이디입니다.'
    }

    if not User.objects.all().filter(username=username):
        data['error'] = False
        data['result'] = '사용 가능한 아이디입니다.'

    return Response(data=data)


class KakaoAccountsLogin(SocialLoginView):
    adapter_class = kakao_views.KakaoOAuth2Adapter
    client_class = OAuth2Client


# 카카오 로그인
@api_view(['GET', 'POST'])
def kakao_login(request):


    REST_API_KEY = '0e63d9a73b29cb9e1c85f0279f834367'
    REDIRECT_URI = 'http://j5a601.p.ssafy.io/login'

    # 인증 코드
    code = request.data['code']
    # print(code)

    # 토큰 요청
    get_token = f'https://kauth.kakao.com/oauth/token'
    params = {
        'grant_type': 'authorization_code',
        'client_id': REST_API_KEY,
        'redirect_uri': REDIRECT_URI,
        'code': code,
    }
    token_res = requests.post(get_token, params=params)
    # print(token_res.json())
    access_token = token_res.json()['access_token']
    # 정보 제공 동의 항목
    scope = token_res.json()['scope']
    # print(scope)
    scope = set(scope.split())
    # print(scope)

    # 프로필 요청
    get_profile = f'https://kapi.kakao.com/v2/user/me'
    header = {
        'Authorization': f'Bearer {access_token}'
    }

    profile_res = requests.get(get_profile, headers=header)

    data = {
        'access_token': access_token
    }
    accept = requests.post(f'http://j5a601.p.ssafy.io:8000/accounts/kakao/user/', data=data)
    # print(accept)

    # 소셜 로그인 유저
    social_user = SocialAccount.objects.all().filter(uid=profile_res.json()['id'])
    # 소셜 로그인과 연결된 유저
    user = get_object_or_404(User, id=social_user.values()[0]['user_id'])

    # 정보 업데이트
    if scope.__contains__('profile_nickname'):
        user.nickname = profile_res.json()['properties'].get('nickname', '')
    else:
        user.nickname = ''

    if scope.__contains__('profile_image'):
        user.profile_img = profile_res.json()['properties'].get('profile_image', '')
    else:
        user.profile_img = ''

    if scope.__contains__('account_email'):
        user.email = profile_res.json()['kakao_account'].get('email', '')
    else:
        user.email = ''

    user.save()

    return Response(accept.json())





