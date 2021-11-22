

# 이리오너라(Irioneora)



## 1️⃣ 프로젝트 소개

1. 일정 : 2021-08-30 ~ 2021-10-08 (총 6주)
   - Sub1 : 2021-08-30 ~ 2021-09-03
   - Sub2 : 2021-09-06 ~ 2021-09-17
   - Sub3 : 2021-09-20 ~ 2021-10-08 
   
   
   
2. 인원 (총 4인)

   

   ![image-20211008052404895](README.assets/image-20211008052404895.png)

<br><br>

## 📋 기술 스택

- SCM 
  - <img src="https://img.shields.io/badge/Gitlab----yellowgreen?logo=gitlab" style="float: left">
- Issue 
  - <img src="https://img.shields.io/badge/Jira----yellowgreen?logo=jira" style="float: left">
- Communication 
  - <img src="https://img.shields.io/badge/Mattermost----yellowgreen?logo=mattermost" style="float: left">
- Design/UI/UX :
  - <img src="https://img.shields.io/badge/Adobe Photoshop----yellowgreen?logo=adobe photoshop" style="float: left">
  - <img src="https://img.shields.io/badge/Figma----yellowgreen?logo=figma" style="float: left">

<br>

- DB
  - <img src="https://img.shields.io/badge/Mysql----yellowgreen?logo=mysql" style="float: left">
- Cloud
  - <img src="https://img.shields.io/badge/AWS-EC2-yellowgreen?logo=amazon aws" style="float: left;">
  - <img src="https://img.shields.io/badge/Ubuntu-20.04.2 LTS-yellowgreen?logo=ubuntu" style="float: left;">
  - <img src="https://img.shields.io/badge/Docker-20.10.7-yellowgreen?logo=docker" style="float: left;">
  - <img src="https://img.shields.io/badge/Nginx-1.18.0-yellowgreen?logo=nginx" style="float: left;">

<br>

**Back-End**

  - <img src="https://img.shields.io/badge/Python-v3.8.10-yellowgreen?logo=python" style="float: left">
  - <img src="https://img.shields.io/badge/Django-v3.2.7-yellowgreen?logo=django"  style="float: left">
  - <img src="https://img.shields.io/badge/Visual Studio Code----yellowgreen?logo=visualstudiocode" style="float: left">

<br>

**Hadoop**

- <img src="https://img.shields.io/badge/Hadoop-v3.2.2-yellowgreen?logo=hadoop" style="float: left">
- <img src="https://img.shields.io/badge/Pyspark-v3.1.2-yellowgreen?logo=pyspark" style="float: left">

<br>

**Front-End**

  - <img src="https://img.shields.io/badge/HTML----yellowgreen?logo=html5"  style="float: left">
  - <img src="https://img.shields.io/badge/SCSS----yellowgreen?logo=sass"  style="float: left">
  - <img src="https://img.shields.io/badge/JavaScript-ES6+-yellowgreen?logo=javascript" style="float: left">
  - <img src="https://img.shields.io/badge/Vue.js-@vue/cli 4.5.13-yellowgreen?logo=vue.js"  style="float: left">
  - <img src="https://img.shields.io/badge/Node.js-v.14.17.3-yellowgreen?logo=node.js" style="float: left">
  - <img src="https://img.shields.io/badge/Visual Studio Code----yellowgreen?logo=visualstudiocode" style="float: left">

<br>



## 기획의도 

#### 1. 우리 문화재에 대한 접근성 높이기 

​		![image-20211008050022799](README.assets/image-20211008050022799.png) 

- 우리나라 문화재와 유물의 매력을 손쉽게 접할 수 있는 서비스 제공

<br>

#### 2. MZ세대의 흥미에 맞춘 테스트 서비스

-  유저들의 흥미를 유발하기 위하여 사용자가 직접 참여하는 테스트를 기획

<br>

<br>

## 프로젝트 아키텍처 

![image-20211008050350006](README.assets/image-20211008050350006.png) 

<br>

<br>

## 분산처리 (Hadoop) 구조

![image-20211008050740247](README.assets/image-20211008050740247.png) 



<br><br>

## 향후 발전 가능성 및 의의 

- 현재 EC2 서버에서 분산처리를 수행하고있으나, 대규모 클러스터를 연결하여 다수의 사용자가 이용할 수 있도록 개선시킬 예정
- 국/공립 박물관과의 서비스 연계 등을 통하여 우리나라 유물과 전통 전반을 소개하는 서비스로 발전 가능 

<br>

<br>

## 🎨 디자인

#### MAIN PAGE

![main-up](README.assets/main-up-3633349.png).![main-down](README.assets/main-down-3633359.png) 

<br>

#### RESULT PAGE

![face-result-1](README.assets/face-result-1.png)![face-result-2](README.assets/face-result-2.png) 

<br>

#### DETAIL PAGE

![detail](README.assets/detail.png) <img src="README.assets/word-cloud.png" alt="word-cloud" /> 

![detail-map](README.assets/detail-map.png) 

<br>

#### SEARCH PAGE

![search-index](README.assets/search-index.png) ![search-filter](README.assets/search-filter.png) 

<br>

#### LOGIN & SIGNUP PAGE  

![login](README.assets/login.png) ![signup](README.assets/signup.png) 

<br>

#### PROFILE PAGE

![profile-like](README.assets/profile-like.png) ![profile-resemble](README.assets/profile-resemble.png) 



<br>

## 2️⃣ 프로젝트 파일 구조

### Back

```
backend
│  
│  manage.py
│  README.md
│  requirements.txt
│  
├─accounts
│  │  adapter.py
│  │  admin.py
│  │  apps.py
│  │  models.py
│  │  serializers.py
│  │  tests.py
│  │  urls.py
│  │  views.py
│  │  __init__.py
│  │  
│  └─migrations
│          
├─artifacts
│  │  admin.py
│  │  apps.py
│  │  models.py
│  │  serializers.py
│  │  tests.py
│  │  urls.py
│  │  views.py
│  │  __init__.py
│  │  
│  └─migrations
│          
├─irioneora
│      asgi.py
│      mysql_settings.py
│      settings.py
│      urls.py
│      wsgi.py
│      __init__.py
│      
├─pages
│  │  admin.py
│  │  apps.py
│  │  models.py
│  │  serializers.py
│  │  tests.py
│  │  urls.py
│  │  views.py
│  │  __init__.py
│  │  
│  └─migrations
│          
├─scripts
│  │  get_vision_data.py
│  │  storing_data.py
│  │  storing_vision_data.py
│  └─ __init__.py
│          
└─spark
    │  admin.py
    │  apps.py
    │  models.py
    │  tests.py
    │  urls.py
    │  views.py
    │  __init__.py
    │  
    ├─migrations
    │      
    └─model
        ├─data
        │      part-00000-a1604de1-63fa-4947-8f13-325cb7ba07d9-c000.snappy.parquet
        │      _SUCCESS
        │      
        └─metadata
                part-00000
                _SUCCESS
```

### Front

```
frontend
│  
│  babel.config.js
│  extt.txt
│  package-lock.json
│  package.json
│  README.md
│  vue.config.js
│  webpack.config.js
│  
├─public
│      favicon.ico
│      index.html
│      logo-navbar.png
│      
└─src
    │  App.vue
    │  main.js
    │  
    ├─api
    │      accounts.js
    │      artifacts.js
    │      kakao.js
    │      
    ├─assets
    │  │  logo.png
    │  │  
    │  ├─images
    │  │      detailpage-cloud.png
    │  │      heart-empty.png
    │  │      heart.png
    │  │      kakao-icon.png
    │  │      kakao-login-wide.png
    │  │      left-m.png
    │  │      logo-main.png
    │  │      logo-navbar.png
    │  │      logo-transparent.png
    │  │      mainpage-flower.png
    │  │      mainpage.png
    │  │      middle-m.png
    │  │      nav-search.png
    │  │      profile-background.png
    │  │      profile-transparent.png
    │  │      result-replay.png
    │  │      result-share.png
    │  │      resultpage-face-left.png
    │  │      resultpage-face-right.png
    │  │      resultpage.png
    │  │      right-m.png
    │  │      right-mountain2.png
    │  │      
    │  └─style
    │      ├─accounts
    │      │      Login.scss
    │      │      profile-sub.scss
    │      │      profile.scss
    │      │      sign-in-up.scss
    │      │      signup.scss
    │      │      _image-box.scss
    │      │      _kakao-login.scss
    │      │      
    │      ├─artifacts
    │      │      detail.scss
    │      │      museum.scss
    │      │      result.scss
    │      │      _card-thumbnail.scss
    │      │      _error-modal.scss
    │      │      _icon-button.scss
    │      │      _result-box.scss
    │      │      _search-box.scss
    │      │      _search-card.scss
    │      │      _search-filter.scss
    │      │      _search-filterpage.scss
    │      │      _search-page.scss
    │      │      _todays-artifact.scss
    │      │      
    │      └─common
    │              button.scss
    │              Error.scss
    │              Loading.scss
    │              main.scss
    │              NavBar.scss
    │              
    ├─components
    │  │  
    │  ├─accounts
    │  │      ImageBox.vue
    │  │      KakaoLogin.vue
    │  │      UserInput.vue
    │  │      
    │  ├─artifacts
    │  │      CardThumbnail.vue
    │  │      ErrorModal.vue
    │  │      IconButton.vue
    │  │      ImageInput.vue
    │  │      MuseumModal.vue
    │  │      ReseultPreview.vue
    │  │      ResultBox.vue
    │  │      SearchBox.vue
    │  │      SearchCard.vue
    │  │      SearchFilter.vue
    │  │      TodaysArtifact.vue
    │  │      
    │  └─common
    │          Button.vue
    │          Loading.vue
    │          LowBar.vue
    │          NavBar.vue
    │          
    ├─router
    │      index.js
    │      
    ├─store
    │  │  index.js
    │  │  
    │  └─modules
    │          accounts.js
    │          artifacts.js
    │          
    └─views
        ├─accounts
        │      LoginPage.vue
        │      ProfileLikePage.vue
        │      ProfilePage.vue
        │      ProfileResemblePage.vue
        │      SignInUpPage.vue
        │      SignupPage.vue
        │      
        ├─artifacts
        │      DetailPage.vue
        │      ResultPage.vue
        │      SearchFilterPage.vue
        │      SearchIndexPage.vue
        │      SearchPage.vue
        │      
        └─common
                ErrorPage.vue
                LoadingPage.vue
                MainPage.vue        

```

