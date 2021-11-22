<template>
  <div>

    <div @click="moveDetail(idNum)" class="search-card">

      <div class="search-card-img">
        <img :src="`${changedUrl}`" alt=""/> 
      </div>

      <div class="search-card-p">
        {{name}}
      </div>

    </div>

  </div>
</template>

<script>
  export default {
    name: 'SearchCard',
    props: ['artifact'],

    data () {
    return {
      imageUrl : '',
      changedUrl : "",
      idNum : '',
      name: ''
      }
    },

    methods: {
      // URL 주소 체인지
      changeUrl (url) {
        if (url === undefined) {
          return false
        } 
        const splitResult = url.split('/',3)
        const sumUrl = 'http://www.emuseum.go.kr' + '/' + splitResult[1] + '/' + splitResult[2]
        this.changedUrl = sumUrl
      },

      // 디테일 페이지로 보내기
      moveDetail (id_num) {
        const target = '/detail/' + String(id_num)
        this.$router.push(target);
      }
    },

    mounted () {
      if (this.artifact === undefined) {
        return false
      }
      this.imageUrl = this.artifact.imgThumUriM
      this.idNum = this.artifact.id
      this.name = this.artifact.name
      this.changeUrl(this.imageUrl)
    }
  }
</script>

<style lang="scss" scoped>
  @import "src/assets/style/artifacts/_search-card.scss";
</style>