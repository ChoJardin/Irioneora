<template>
  <div id="app">
    <NavBar id="app-nav"/>

    <div id="app-content">
      <router-view/>
    </div>

    <LowBar id="low-bar"></LowBar>
  </div>
</template>

<script>  
import cookies from "vue-cookies";
import AccountsApi from "@/api/accounts";

import NavBar from './components/common/NavBar.vue'
import LowBar from "@/components/common/LowBar";

export default {
  components: {
    NavBar,
    LowBar
  },
  created() {
    // 로그인된 유저 확인
    const token = cookies.get('user-token')

    if (token) {
      AccountsApi.requestProfile(token)
      .then(res => {
        this.$store.dispatch('setProfileInfo', res.data)
      })
    }
  }
}
</script>

<style>
#app {
  max-width: 425px;
  width: 100%;
  /* 가운데 정렬 */
  position: absolute;
  left: 0;
  right: 0;
  margin: 0 auto;

  /* 임시로 구분선 하나 그을게요.. */
  border: 1px solid ivory;

  font-family: 'Noto Serif KR', serif;

}

#app-content {
  min-height: calc(100vh - 130px);
  /*margin-top: 40px;*/
  margin-bottom: 60px;
  margin-top: 70px;
}

#app-nav {
  /*padding: 30px;*/
}

#low-bar {
  position: absolute;
  bottom: 0;
}

</style>
