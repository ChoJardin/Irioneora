<template>
  <div @click="$router.push(`/detail/${result.identification}`)">
    <div class="result-box-wrap">
      
      <div class="explian-text">
        사진과 닮은 문화재 속 인물입니다.
      </div>
      <div class="artifact-image-wrap">
        <img v-if="result.url" :src="imageUri" alt="" class="artifact-image">
        <img v-else src="@/assets/images/mainpage.png" alt="" class="artifact-image">
        <div class="artifact-image-crop" :style="artifactImageCrop"></div>
      </div>

      <div class="artifact-description">
        <div class="artifact-number">
          {{number}}
        </div>
        <div class="artifact-name">
          {{result.name}}
        </div>
      </div>
      
    </div>
  </div>
</template>

<script>
import ArtifactsApi from "@/api/artifacts";

export default {
  name: "ResultBox",
  props: ['number', 'result'],
  methods: {
    onClick() {

    }
  },
  computed: {
    imageUri() {
      return `https://${this.result.url}`
    },
    artifactImageCrop() {
      return {
        '--crop-start-x': this.result.x,
        '--crop-start-y': this.result.y,
        '--crop-width': this.result.w,
        '--crop-height': this.result.h,
        '--image-width': this.result.width,
        '--image-height': this.result.height,
      }
    }
  },
}
</script>

<style lang="scss" scoped>
  @import "src/assets/style/artifacts/_result-box";
</style>