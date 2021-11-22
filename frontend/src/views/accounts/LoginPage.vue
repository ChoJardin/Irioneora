<template>
  <div id="login">

    <div class="login-input">

    <UserInput class="user-input"
        id="username" label="아이디" placeholder="아이디를 입력하세요" type="text"
        :input.sync="username" :error="error.username"
        @keyup-enter="moveFocusToPw" @on-focus="onFocus" ref="username"/>

    <UserInput class="user-input"
        id="password" label="비밀번호" placeholder="비밀번호를 입력하세요" type="password"
        :input.sync="password" :error="error.password"
        @keyup-enter="onLogin" @on-focus="onFocus" ref="password"/>
    </div>

    <div v-if="loginError.isFailed" class="error-message">
      {{ loginError.message }}
    </div>

    <button class="button" :disabled="!isSubmit" @click="onLogin">로 그 인</button>

    <KakaoLogin class="kakao-login-long"></KakaoLogin>



  </div>
</template>

<script>
import cookies from "vue-cookies";
import PV from "password-validator"
import AccountsApi from "@/api/accounts";
import UserInput from "@/components/accounts/UserInput";
import KakaoLogin from "@/components/accounts/KakaoLogin";

export default {
  name: "Login",
  // components
  components: {
    UserInput,
    KakaoLogin
  },
  // props
  // data
  data() {
   return {
     username: "",
     password: "",
     passwordSchema: new PV(),
     autoLogin: false,
     error: {
       username: false,
       password: false
     },
     isSubmit: false,
     loginError: {
       isFailed: false,
       message: "입력하신 정보와 일치하는 아이디 혹은 비밀번호가 존재하지 않습니다."
     },
   }
  },
  // methods
  methods: {
    // 형식 검증
    checkForm() {
      // 아이디, 비밀번호 입력됐으면 버튼 활성화
      if (this.password && this.username)
        this.isSubmit = true

    },

    // 로그인
    onLogin() {
      if (this.isSubmit) {
        let {username, password} = this
        let data = {
          username,
          password,
        }

        // 버튼 비활성화
        this.isSubmit = false
        AccountsApi.requestLogin(data)
          // 로그인 성공
          .then(res => {
            const token = res.data.key
              // 회원 프로필 저장
              AccountsApi.requestProfile(token)
                .then(res => {
                  this.$store.dispatch('setProfileInfo', res.data)
                })
              // 쿠키에 유저 토큰 저장
              this.$store.dispatch('fulfillLogin', token)
              // .then( res => {
                // cookies.set('user-token', token, 0)
                // this.$router.go(-1)
              // }
              // )
            })
            .then(res => this.$router.push('/profile'))

          // 로그인 실패
          .catch(() => {
            this.loginError.isFailed = true
            this.$refs.username.onReset()
            this.$refs.password.onReset()
          })
      }
    },

    // 로그인 실패 에러메시지가 노출되어 있을 때,
    // 새로 로그인을 시도하는 경우, 해당 메시지 사라지도록
    onFocus() {
      this.loginError.isFailed = false
    },

    // 입력 칸 포커스 이동
    moveFocusToPw() {
      document.getElementById('username').blur()
      document.getElementById('password').focus()
    },
  },
  // computed
  computed: {
    isLoggedIn() {
      return this.$store.getters.isLoggedIn
    }
  },
  // watch
  watch: {
    username: function () {
      // 대문자 입력 방지
      this.username = this.username.toLowerCase()
    },
    password: function () {
      this.checkForm()
    },
  },
  // lifecycle hook
  //navigation guard
}
</script>

<style lang="scss" scoped>
 @import "src/assets/style/accounts/Login";
</style>