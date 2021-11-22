<template>
  <div>
    <div class="router-wrap">
      <router-link to="/login" class="router" replace>로그인</router-link>
      <router-link to="/signup" class="router" replace>회원가입</router-link>
    </div>

    <router-view></router-view>

  </div>
</template>

<script>
export default {
  name: "SignInUpPage"
}
</script>

<style lang="scss" scoped>
  @import "src/assets/style/accounts/sign-in-up";
</style>