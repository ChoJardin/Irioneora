import axios from 'axios'

// const URL = 'http://localhost:8000/'
const URL = 'http://j5a601.p.ssafy.io:8000/'

const ROUTES = {
  profile: 'rest-auth/user/',
  login: 'rest-auth/login/',
  kakao: 'accounts/kakao/login/',
  userFace: 'spark/userface/',
  usernameCheck: 'accounts/username/',
  signup: 'rest-auth/signup/'
}

// 프로필 정보 요청
async function requestProfile (token) {
  const profilePath = URL + ROUTES.profile
  const headers = {
    'Authorization': `Token ${token}`
  }
  return await axios.get(profilePath, {headers: headers})
}

async function requestLogin(data) {
  const loginPath = URL + ROUTES.login
  return await axios.post(loginPath, data)
}

// 카카오 로그인
async function requestKakaoLogin(code) {
  const kakaoPath = URL + ROUTES.kakao
  const data = {
    'code': code
  }
  console.log('request')
  return await axios.post(kakaoPath, data)
}

// 얼굴 데이터 백 전송
async function requestAnalyze(data) {
  const analyzePath = URL + ROUTES.userFace
  return await axios.post(analyzePath, data)
}

// 아이디 중복확인
async function requestUsernameCheck(params) {
  const usernameCheckPath = URL + ROUTES.usernameCheck
  return await axios.get(usernameCheckPath, {params: params})
}

// 회원가입
async function requestSignup(data) {
  const signupPath = URL + ROUTES.signup
  return await axios.post(signupPath, data)
}



const AccountsApi = {
  URL,
  ROUTES,
  requestProfile: (token) => requestProfile(token),
  requestLogin: (data) => requestLogin(data),
  requestAnalyze: (data) => requestAnalyze(data),
  requestKakaoLogin: (code) => requestKakaoLogin(code),
  requestUsernameCheck: (params) => requestUsernameCheck(params),
  requestSignup: (data) => requestSignup(data),
}

export default AccountsApi