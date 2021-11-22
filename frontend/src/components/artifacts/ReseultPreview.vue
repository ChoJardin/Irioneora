<template>
  <div>
    <div class="img-wrap">
      <img v-if="preview" :src="preview" alt="profile image">
      <img v-else src="@/assets/images/logo-main.png" alt="profile image">
    </div>
  </div>
</template>

<script>
import {mapState} from "vuex";

export default {
  name: "ResultPreview",
  computed: {
    ...mapState({
      preview: state => state.artifacts.preview
    })
  },
}
</script>

<style lang="scss" scoped>
  @import "src/assets/style/accounts/_image-box";
</style>