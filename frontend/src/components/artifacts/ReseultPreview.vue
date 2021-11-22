<template>
  <div>
    <div class="img-wrap">
      <div class="img-container">
        <img v-if="preview" :src="preview" :style="previewImgClip" alt="preview image" class="img-preview">
        <img v-else src="@/assets/images/logo-main.png" alt="preview image" class="img-profile">
      </div>
    </div>
  </div>
</template>

<script>
import {mapState} from "vuex";

export default {
  name: "ResultPreview",
  computed: {
    ...mapState({
      preview: state => state.artifacts.preview,
      kakaoResult: state => state.accounts.kakaoResult
    }),
    calculMargin() {
      if( this.kakaoResult.height <= this.kakaoResult.width) {
        return 0
      } else {
        return String(-100 * this.kakaoResult.faces[0].y) + '%'
      }
    },
    previewImgClip() {
      return {
        '--face-start-x': this.kakaoResult.faces[0].x * 100,
        '--face-start-y': this.kakaoResult.faces[0].y,
        '--face-width': this.kakaoResult.faces[0].w,
        '--face-height': this.kakaoResult.faces[0].h,
        '--image-width': this.kakaoResult.width,
        '--image-height': this.kakaoResult.height,
        '--margin-start': this.kakaoResult.width * this.kakaoResult.faces[0].x - 30,
        '--margin-end': this.kakaoResult.width * (this.kakaoResult.faces[0].x + this.kakaoResult.faces[0].w) + 30,
        '--margin-up': this.calculMargin,
        '--margin-down': String(100 - (100 * (this.kakaoResult.faces[0].y + this.kakaoResult.faces[0].h) )) + '%'
      }
    }
  },
}
</script>

<style lang="scss" scoped>
  @import "src/assets/style/accounts/_image-box";
</style>