<template>
  <div class="result">
    <div class="result-preview">
      <img src="@/assets/images/resultpage-face-left.png" alt="" class="face-left">
      <ResultPreview></ResultPreview>
      <img src="@/assets/images/resultpage-face-right.png" alt="" class="face-right">
    </div>

    <div class="result-box-wrap">
      <span class="material-icons-outlined arrow left" @click="moveBackward">arrow_back_ios</span>
      <transition :name="slideTransition" mode="out-in">
        <ResultBox v-if="nowShowing===1" :result="results[0]" number="1" class="result-box" key="1"></ResultBox>
        <ResultBox v-else-if="nowShowing===2" :result="results[1]" number="2" class="result-box" key="2"></ResultBox>
        <ResultBox v-else-if="nowShowing===3" :result="results[2]" number="3" class="result-box" key="3"></ResultBox>
        <ResultBox v-else-if="nowShowing===4" :result="results[3]" number="4" class="result-box" key="4"></ResultBox>
      </transition>
      <span class="material-icons-outlined arrow right" @click="moveForward">arrow_forward_ios</span>
    </div>

    <div class="icon-button-wrap">
      <IconButton
          value="다시하기" @click.native="onRedo"
          icon="https://irioneora.s3.ap-northeast-2.amazonaws.com/result-replay.png" class="icon-button"></IconButton>
      <IconButton @click.native="kakaoRequest()" value="공유하기" icon="https://irioneora.s3.ap-northeast-2.amazonaws.com/result-share.png" class="icon-button"></IconButton>
    </div>

  </div>
</template>

<script>
import ResultPreview from "@/components/artifacts/ReseultPreview";
import ResultBox from "@/components/artifacts/ResultBox";
import IconButton from "@/components/artifacts/IconButton";
import {mapState} from "vuex";

export default {
  name: "ResultPage",
  components: {
    ResultPreview,
    ResultBox,
    IconButton
  },
  data() {
    return {
      nowShowing: 1,
      slideTransition: 'slide-right',

      // 세일이 만듬
      selectedUrl: '',
      cuttedUrl: 'www.emusueu/openapi/img?serviceKey=YRxuikhcQX7v7M0GurZEBdHr49zxbr2so054TqRBKqRBZzBQo7xWyhdM06W8QSsVLjQyaRpV%2BM8oRktGCkQ8oFx2VKjYUUqoOG7rRO2tJXcxleSenoyroumw7aVcXof9F7egXUi1K%2F4%3D&imageId=YjNLeE1CdGR6RUZUckU5ZllIbnU0SmVRbHFvZkxoZy9YNU9BeW5scWlRcXZrZTMxWUNsTGNBc2M2cUtpRmRoaHFqTEs5TnlJUnAvTzlkTHpVbnVZMmtZaytHRnYwQldM',
      kakaoImageUrl: null,
    }
  },
  methods: {
    // 이전 결과 보기
    moveBackward() {
      this.slideTransition = 'slide-left'

      if (this.nowShowing === 1) {
        this.nowShowing = 4
      } else this.nowShowing--

      const transition = document.getElementById('transition')
      console.log(transition)
    },
    // 다음 결과 보기
    moveForward() {
      this.slideTransition = 'slide-right'

      if (this.nowShowing === 4) {
        this.nowShowing = 1
      } else this.nowShowing++
    },

    // 다시하기
    onRedo() {
      this.$router.push('/')
    },

    //세일이 만듬

    karequest () {
      console.log('aaa')
    },

    // logic 
    // 1. url을 받아와서 'http://www.emuseum.go.kr/'을 잘라야함 그래야 proxy설정이 맞아서 통신이 된다.
    // 2. 자른 url을 받아서 파일로 만들고 변환해야함
    // 3-1. 해당 파일을 카카오의 업로드하여 업로드 주소를 받음
    // 3-2. 해당 주소를 공유하기 ImageUrl에 넣으면 완료!

    // 카카오 공유하기
    async kakaoRequest () {
      // console.log(1)
      // 1. url 자르기
      this.selectedUrl = this.cuttingUrl
      console.log(this.selectedUrl)
     
      const splitResult = this.selectedUrl.split('/',3)
      const sumUrl = '/' + splitResult[1] + '/' + splitResult[2]
      this.cuttedUrl = sumUrl
      
      // this.cuttedUrl = this.selectedUrl.substring(13,this.selectedUrl.length)
      console.log(this.cuttedUrl)
      console.log('중간평가')

      // 2.url을 받아서, 파일 생성에 맞는 형식으로 변환
      const response = await fetch(this.cuttedUrl);
      const blob = await response.blob();

      // 파일 생성하기
      const file = new File([blob], 'image.jpg', {type: blob.type});
      let list = new DataTransfer();
      list.items.add(file);
      let myFileList = list.files;

      // 3-1. 위에서 만든 파일을 통해서 카카오 url 등록하기
      var files = myFileList
      await window.Kakao.Link.uploadImage({
        file: files
      })
      .then((res) =>{

        // 수정 카카오 url을 저장해야함
        this.kakaoImageUrl = res.infos.original.url
        console.log(this.kakaoImageUrl)
      })
      .catch((err) => {
        console.log(err)
      })
      
      // 3-2.공유하기
      window.Kakao.Link.sendDefault({ 
        objectType: 'feed', 
        content: { 
          title: '나와 닮은 얼굴은????', 
          description: '지금 바로 나와 닮은 문화재를 찾아보세요!', 
          imageUrl: this.kakaoImageUrl,
          link: { 
            mobileWebUrl: 'http://j5a601.p.ssafy.io/', 
            webUrl: 'http://j5a601.p.ssafy.io/', 
              }, 
            }, 
          buttons: [{ 
            title: '이리오너라!!', 
            link: { 
              mobileWebUrl: 'http://j5a601.p.ssafy.io/', 
              webUrl: 'http://j5a601.p.ssafy.io/', 
              },
            }], 
        }) 
        
      }, 
  
  },
  computed: {

    ...mapState({
      results: state => state.artifacts.results
    }),

    cuttingUrl (){
      console.log('computed')
      console.log(this.results)
      console.log(this.nowShowing-1)
      console.log(this.results[this.nowShowing-1])
      return this.results[this.nowShowing-1].url
    }
  }
}
</script>

<style lang="scss" scoped>
  @import "src/assets/style/artifacts/result";

</style>