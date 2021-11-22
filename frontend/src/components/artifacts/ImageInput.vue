<template>
  <div>
    <input id="image-input" ref="imgInput" type="file" accept="image/jpeg, image/png"
       @change="onImageUploaded" >
  </div>
</template>

<script>
import KakaoApi from "@/api/kakao";
import AccountsApi from "@/api/accounts";

export default {
  name: "ImageInput",
  props: ['preview'],
  data() {
    return {
      selectedFile: null,
      error: '',
    }
  },
  methods: {
    // input창 호출
    onOpen() {
      this.$refs.imgInput.click()
    },

    // error 초기화
    onReset() {
      this.error = ''
    },

    // kakao vision -> back으로 얼굴 json 전송
    async requestAnalyze (imageFile) {
      // kakao 얼굴 데이터 검출
      const res = await KakaoApi.requestFacialData(imageFile)
      // 얼굴 데이터를 검출하지 못한 경우
      if (res.data.result.faces.length === 0) {
        this.$emit('on-error', '얼굴이 없거나, 확인이 불가합니다.')
        this.$emit('on-loading', false)
        throw new Error('face not detected');
      }
      // 얼굴 데이터를 전송받은 경우
      else {
        // console.log(res.data.result)
        this.$store.dispatch('setKakaoResult', res.data.result)
        const result = await AccountsApi.requestAnalyze(res.data)
        return result
      }
    },

    // 미리보기
    async setPreview(data) {
      return await this.$store.dispatch('setPreview', data)
    },

    // 이미지 입력 받음
    onImageUploaded(event) {
      // 로딩 스피너 돌기
      this.$emit('on-loading', true)

      this.selectedFile = event.target.files[0]
      // 이미지 확장자/ 크기 확인
      let extension = this.selectedFile.name.substring(
          this.selectedFile.name.lastIndexOf('.')+1
      ).toLowerCase()

      // 이미지 파일이 아닌 경우
      // console.log(extension)
      if (!['jpg', 'jpeg', 'png'].includes(extension)) {
        this.error = '이미지 파일을 선택해 주세요.'
      }
      // 파일의 크기가 너무 큰 경우
      else if (this.selectedFile.size > 2097152) {
        this.error = '2MB 이내의 파일만 선택 가능합니다.'
      }

      // 에러 발생하면 에러메세지 emit
      if (this.error) {
        this.$emit('on-error', this.error)
        this.$emit('on-loading', false)
      }

      // 오류 없는 경우 formData 전송
      else {
        // 서버 전송 데이터
        const imageFile = new FormData()
        imageFile.append('image', this.selectedFile)

        this.requestAnalyze(imageFile)
          .then(res => {
            // vuex 결과 저장
            this.$store.dispatch('setResults', res.data)

            // 미리보기
            const read = new FileReader()
            read.onload = file => {
              this.setPreview(file.target.result)
                .then(() => {
                  this.$router.push('/result')
                  this.$emit('on-loading', false)
                })
            }
            read.readAsDataURL(this.selectedFile)
            // console.log(res)

          })
        .catch(err => {
          this.$emit('on-error', '얼굴이 없거나, 확인이 불가합니다.')
          this.$emit('on-loading', false)
        })




      }
    }

  }

}
</script>

<style scoped>

</style>