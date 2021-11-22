import cookies from "vue-cookies";
import ArtifactsApi from "@/api/artifacts";

const state = {
  authToken: cookies.get('user-token'),
  // 프로필
  profileInfo: {
    username: '',
    nickname: '',
    profile_img: '',
    like_artifact: [
      {
        id: '',
        identification_number: '',
        image_uri: '',
      }
    ],
    resemble_artifact: [
      {
        id: '',
        identification_number: '',
        image_uri: '',
      }
    ]
  },
}
const getters = {
  isLoggedIn: state => !!state.authToken,
  config: state => ({ headers: { Authorization: `Token ${state.authToken}` }}),
}
const mutations = {
  SET_PROFILE_INFO(state, profile) {
    state.profileInfo = profile
  },
  LOGOUT(state) {
    state.authToken = ''
  }
}
const actions = {
  setProfileInfo({commit}, profile) {
    commit('SET_PROFILE_INFO', profile)
  },

  // 로그인
  // 토큰 저장 & 닮은 유물 저장 요청
  async fulfillLogin({commit, state, rootState}, token) {
    console.log('im here')
    // 쿠키에 토큰 저장
    cookies.set('user-token', token, 0)
    // 닮은 유물 저장 요청 -> 앞서 요청 보낸 경우가 있었다면,
    const identification_number = rootState.artifacts.results[0].identification
    if (!identification_number) {
      return true
    } else {
      console.log('need save')
      ArtifactsApi.saveResembleArtifact('PS0100100101600242200000')
        .then(res => true)
        // 저장이 안되더라도 로그인은 된 거니까 그냥 넘어가겠습니다..
        .catch(err => true)
    }
  },
  logout({commit}) {
    commit('LOGOUT')
    cookies.set('user-token', '', 0)
  }
}


export default {
  state, getters, mutations, actions
}