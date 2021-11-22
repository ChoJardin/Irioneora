<template>
  <div>
    <button @click.prevent="onClick" class="kakao-button">
      <img src="@/assets/images/kakao-icon.png" alt="">
      &nbsp;
      카카오 로그인
    </button>
  </div>
</template>

<script>
import AccountsApi from "@/api/accounts";
import cookies from "vue-cookies";

export default {
  name: "KakaoLogin",
  methods: {
    onClick() {
      const REDIRECT_URI = 'http://j5a601.p.ssafy.io/login'
      const REST_API_KEY = '0e63d9a73b29cb9e1c85f0279f834367'
      const kakao_redirect = `https://kauth.kakao.com/oauth/authorize?client_id=${REST_API_KEY}&redirect_uri=${REDIRECT_URI}&response_type=code`
      window.location.href = kakao_redirect
    }
  },
  watch: {
    '$route.query.code': {
        handler: function(code) {
          if (code) {
            AccountsApi.requestKakaoLogin(code)
            .then(res => {
              this.$store.dispatch('fulfillLogin', res.data.key)
              cookies.set('user-token', res.data.key)
              this.$router.push('/')
              // this.$router.go(-2)
            })
          }
        },
        deep: true,
        immediate: true
      }
  }
}
</script>

<style lang="scss" scoped>
 @import "src/assets/style/accounts/_kakao-login";
</style>