<template>
  <div class="main">
    <img src="@/assets/images/mainpage.png" alt="main page image" class="background">
    <img src="@/assets/images/mainpage-flower.png" alt="" class="flower">
    <div class="description">
      <div class="description-kr">
        이리오너라에서<br>
        조금 더 쉽고, 조금 더 재미있게<br>
        다양한 문화재를 만나보세요!
      </div>
      <div class="description-eng">
        WELCOME <br>
        TO
      </div>
    </div>

    <!-- 이미지 입력/ 안내 -->
    <div class="image-upload">
      <Button id="flux" value="나와 닮은 문화재 찾기 →" class="button" @click.native="onImage"></Button>

      <ImageInput
          class="image-input" ref="image"
          @on-loading="onLoading" @on-error="onError">
      </ImageInput>
      <!-- 사진 에러-->
      <ErrorModal v-if="isError" @close="isError=false" :error="error"></ErrorModal>
      <div class="info">
        사진은 저장되지 않습니다.<br>
        얼굴이 흐릿하게 나오거나, 판별하기 어려운 사진은 결과가 도출되지 않을 수 있습니다.
      </div>
    </div>

    <!-- 오늘의 문화재 -->
    <div class="todays-artifact">
      오늘의 문화재
      <TodaysArtifact></TodaysArtifact>
    </div>

    <!-- 로딩 스피너 -->
    <Loading v-if="isLoading" class="loading"></Loading>

  </div>
</template>

<script>
import Button from "@/components/common/Button";
import ImageInput from "@/components/artifacts/ImageInput";
import TodaysArtifact from "@/components/artifacts/TodaysArtifact";
import Loading from "@/components/common/Loading";
import ErrorModal from "@/components/artifacts/ErrorModal";

export default {
  name: "MainPage",
  components: {
    Button,
    ImageInput,
    TodaysArtifact,
    Loading,
    ErrorModal
  },
  data() {
    return {
      isLoading: false,
      isError: false,
      error: ''
    }
  },
  methods: {
    // input 호출
    onImage() {
      this.$refs.image.onOpen()
      this.$refs.image.onReset()
    },
    // 로딩 스피너
    onLoading(status) {
      // console.log(status)
      this.isLoading = status
    },
    onError(error) {
      this.error = error
      this.isError = true
    }
  }
}
</script>

<style lang="scss" scoped>
 @import "src/assets/style/common/main";

</style>