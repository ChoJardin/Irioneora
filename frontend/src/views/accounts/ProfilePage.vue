<template>
  <div>
    <ImageBox></ImageBox>

    <div class="nickname">
      {{nickname}}
      <span @click="onLogout" class="logout">로그아웃</span>
    </div>


    <div class="router-wrap">
      <router-link to="/profile" class="router-button">
        <Button value="좋아하는 문화재" class="button"></Button>
      </router-link>
      <router-link to="/profile/resemble" class="router-button">
        <Button value="나와 닮은 유물" ></Button>
      </router-link>
    </div>
    <router-view></router-view>
  </div>
</template>

<script>
import cookies from "vue-cookies";
import {mapState} from "vuex";
import AccountsApi from "@/api/accounts";
import Button from "@/components/common/Button";
import ImageBox from "@/components/accounts/ImageBox";

export default {
  name: "ProfilePage",
  components: {
    Button,
    ImageBox,
  },
  // props
  // data
  // methods
  methods: {
    onLogout() {
      this.$store.dispatch('logout')
      .then(res =>
        this.$router.push('/')
      )
    }
  },
  // computed
  computed: {
    ...mapState({
      nickname: state => state.accounts.profileInfo.nickname
    })
  },
  // watch
  // life cycle hook
  // navigation guard
  beforeRouteEnter(to, from, next) {
    const token = cookies.get('user-token')
    // 토큰이 있다면
    if (token) {
      next(vm => {
        AccountsApi.requestProfile(token)
          .then(res => {
            // console.log(res.data)
            vm.$store.dispatch('setProfileInfo', res.data)
          })
      })
    }
    else next('/login')
  }
}
</script>

<style lang="scss" scoped>
  @import "src/assets/style/accounts/profile.scss";
</style>