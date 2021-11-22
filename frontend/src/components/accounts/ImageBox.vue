<template>
  <div>
    <div class="img-wrap">
      <div class="img-container">
        <img v-if="profileImg" :src="profileImg" alt="profile image" class="img-profile">
        <img v-else src="@/assets/images/profile-background.png" alt="profile image" class="img-profile">
      </div>
    </div>
  </div>
</template>

<script>
import {mapState} from "vuex";

export default {
  name: "ImageBox",
  // components
  // props
  // data
  // methods
  // computed
  computed: {
    ...mapState({
      profileImg: state => state.accounts.profileInfo.profile_img
    })
  },
  // watch
  // life cycle hook
  // navigation guard
}
</script>

<style lang="scss" scoped>
  @import "src/assets/style/accounts/_image-box";
</style>