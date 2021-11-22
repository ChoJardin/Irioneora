<template>
  <div>
    <div class="detail-page">
      <!-- artifact Info -->
      <div>
        <div class="artifact-name">
          {{ detailInfo.artifact_name }}
        </div>
        <div>
          <img v-if="imgUrl === 'https://www.emuseum.go.kr/'" src="@/assets/images/logo-main.png" class="artifact-image">
          <img v-else :src="imgUrl" class="artifact-image">
        </div>
        <div class="first-tab">
          <div class="second-tab">
            <span class="artifact-title">소장위치</span>
            <span class="artifact-content">{{ detailInfo.museum_name }}</span>
            <button class="museum-button" @click="[openMuseumModal(detailInfo.museum_name), setMuseumInfo(detailInfo.museum_name)]"><span class="museum-button-text">자세히 보기</span></button>
          </div>
        <div v-if="isLoggedIn">
          <div v-if="isLike" class="second-tab">
            <img src="@/assets/images/heart.png" class="heart" @click="likeArtifact(detailInfo.identification_number)">
          </div>
          <div v-if="!isLike" class="second-tab">
            <img src="@/assets/images/heart-empty.png" class="heart" @click="likeArtifact(detailInfo.identification_number)">
          </div>
        </div>
        </div>
        <div>
          <img src="@/assets/images/detailpage-cloud.png" class="detail-bgimg">
        </div>
        <div class="tab">
          <span class="artifact-title">작가</span>
          <span class="artifact-content">{{ detailInfo.artifact_author }}</span>
        </div>
        <div class="tab">
          <span class="artifact-title">시대</span>
          <span class="artifact-content">{{ detailInfo.nationality_name }}</span>
        </div>
        <div class="tab">
          <span class="artifact-title">사이즈</span>
          <span class="artifact-content">{{ detailInfo.artifact_size }}</span>
        </div>
        <div class="tab">
          <span class="artifact-title">색인어</span>
          <span class="artifact-content">{{ detailInfo.index_words }}</span>
        </div>
        <div>
          <div class="artifact-title">설명</div>
          <div class="description">{{ detailInfo.description }}</div>
        </div>
      </div>
      <br>

      <!-- word cloud -->
      <div>
        <div class="wordcloud">
          WORD CLOUD
        </div>
        <div id="wordcloud"></div>
      </div>
    </div>
  </div>
</template>
<script>
import axios from 'axios'
import ArtifactAPI from '@/api/artifacts.js'
import AccountsAPI from '@/api/accounts.js';
import * as echarts from 'echarts'
import 'echarts-wordcloud'
import MuseumModalVue from '../../components/artifacts/MuseumModal.vue'
import {mapState, mapGetters, mapActions} from "vuex";


export default {
  name: 'DetailPage',
  components: { },
  props: '',
  data() {
    return {
      detailInfo: [],
      imgUrl: 'https://',
      isLike: '',
      wordcloudData: '',
    }
  },
  methods: {
    ...mapActions(['setMuseumInfo', 'likeArtifact']),

    // detail page 전체 정보 받아오기
    fetchDetailInfo() {
      axios({
        url: ArtifactAPI.URL + ArtifactAPI.ROUTES.detail + `${this.$route.params.artifactId}`,
        method: 'get',
      })
      .then((res) => {
        this.detailInfo = res.data
        this.imgUrl += res.data.image_uri
      })
      .catch((err) => console.log(err))
    },
    
    // 유물 좋아요
    likeArtifact(artifact_id) {
      axios({
        url: ArtifactAPI.URL + ArtifactAPI.ROUTES.detail + `${artifact_id}/like/`,
        method: 'POST',
        headers: { Authorization: `Token ${this.accessToken}`}
      })
      .then((res) => {
        AccountsAPI.requestProfile(this.accessToken)
        // 저장 작업 따로 필요
        .then((res) => {
          this.$store.dispatch('setProfileInfo', res.data)
          this.isLikeArtifact(this.detailInfo.identification_number)
        })
      })
      .catch((err) => console.log(err))
    },

    // 좋아요한 유물인지 아닌지
    isLikeArtifact(artifact_id) {
      // some 내장함수로 check
      this.isLike = this.likeArtifacts.some(elem => elem.identification_number === artifact_id)
    },

    // 박물관 모달 open
    openMuseumModal() {
      this.setMuseumInfo(this.detailInfo.museum_name);
      this.$modal.show(
        MuseumModalVue,
        {
          modal: this.$modal,
        },
        {
          name: 'dynamic-modal',
          width: '300px',
          height: '500px',
          draggable: false
        }
      )
    },

    // wordcloud 단어 받아오기
    getWordCloud() {
      axios({
        url: ArtifactAPI.URL + ArtifactAPI.ROUTES.detail + `${this.$route.params.artifactId}` + '/wordcloud',
        method: 'get',
      })
      .then((res) => {
        this.wordcloudData = res.data
        this.makeWordCloud()
      })
      .catch((err) => console.log(err))
    },

    // wordcloud 그리기
    makeWordCloud() {
      var chart = echarts.init(document.getElementById('wordcloud'));

      chart.setOption({
          series: [{
              type: 'wordCloud',
              // circle (default),  cardioid (apple or heart shape curve), diamond, triangle-forward, triangle, alias of triangle-upright, pentagon, and star.
              shape: 'pentagon',
              // maskImage: maskImage,
              left: 'center',
              top: 'center',
              width: '90%',
              height: '90%',
              right: 'center',
              bottom: 'center',
              sizeRange: [12, 30],
              rotationRange: [-90, 90],
              rotationStep: 45,
              gridSize: 8,
              drawOutOfBound: false,
              layoutAnimation: true,
              textStyle: {
                  fontFamily: 'Noto Serif KR',
                  fontWeight: 500,
                  color: function(a) {
                    const i =  (a.dataIndex)%6;
                    const color_palette = ['#F1E8DB', '#DEC8A4', '#D5D3C3', '#D4AB67', '#B1AFB2', '#848063'];
                    return color_palette[i];
                  }
              },
              emphasis: {
                  focus: 'self',
                  textStyle: {
                      textShadowBlur: 10,
                      textShadowColor: '#333'
                  }
              },
              data: this.wordcloudData
          }]
      });
    }
  },
  computed: {
    ...mapState({
      accessToken: (state) => state.accounts.authToken,
      likeArtifacts: (state) => state.accounts.profileInfo.like_artifact,
      museumInfo: state => state.artifacts.museumInfo,
    }),
    ...mapGetters(['isLoggedIn'])
  },
  created() {
    this.getWordCloud();
    this.fetchDetailInfo();
    this.isLikeArtifact(this.$route.params.artifactId);
    if (this.isLoggedIn) {
      AccountsAPI.requestProfile(this.accessToken);
    }
  },
}

</script>

<style lang="scss" scoped>
  @import "src/assets/style/artifacts/detail.scss";
</style>