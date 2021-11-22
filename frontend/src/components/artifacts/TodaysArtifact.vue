<template>
  <div class="todays-artifact">
    <div class="image-wrap" @click="onClick">
      <img :src="`https://${imgUri}`" alt="">
    </div>

    <div class="artifact-description">
      <div class="museum">{{museum}}</div>
      <div class="name">{{name}}</div>
      <div class="epoque">{{epoque}}</div>
      <div class="text-description">{{description}}</div>
    </div>
  </div>
</template>

<script>
import ArtifactsApi from "@/api/artifacts";
// import axios from "axios";

export default {
  name: "TodaysArtifact",
  data() {
    return {
      idNumber: '',
      imgUri: '',
      museum: '',
      name: '',
      nationailty: '',
      epoque: '',
      description: '',

    }
  },
  methods: {
    // async gettodayArtifact() {
    //   const res = await ArtifactsApi.requestToday()
    //   return res.data.identificationNumber
    // },

    onClick() {
      this.$router.push(`/detail/${this.idNumber}`)
    }
  },
  created() {
    // 오늘의 문화재
    // this.gettodayArtifact()
    // .then(id => {
    //   const museumApiPath = `/openapi/relic/detail?serviceKey=${ArtifactsApi.SERVICE_KEY}&id=${id}`
    //   console.log(museumApiPath)
    //   axios({
    //     methods: 'get',
    //     url: museumApiPath
    //   })
    //   .then(res => console.log(res))
    //
    // })

    ArtifactsApi.requestToday()
      .then(res => {
        // console.log(res)
        // console.log(res.data.nationality_name)
        this.idNumber = res.data.id_num
        this.imgUri = res.data.image_uri
        this.museum = res.data.museum_name
        this.name = res.data.name
        this.epoque = res.data.nationality_name
        this.description = res.data.desc
        // const recommend = JSON.parse(res.data)
        // // console.log(recommend)
        // // console.log(recommend.result.list.data.item)
        // const artifactInfos = recommend.result.list.data.item
        // artifactInfos.forEach(info => {
        //   // console.log(info)
        //   if (info['@key'] === 'id') {
        //     this.idNumber = info['@value']
        //   } else if (info['@key'] === 'imgUri') {
        //     this.imgUri = info['@value']
        //   } else if (info['@key'] === 'museumName2') {
        //     this.museum = info['@value']
        //   } else if (info['@key'] === 'nameKr') {
        //     this.name = info['@value']
        //   } else if (info['@key'] === 'nationalityName2') {
        //     this.epoque = info['@value']
        //   } else if (info['@key'] === 'nationalityName1') {
        //     this.nationailty = info['@value']
        //   } else if (info['@key'] === 'desc') {
        //     this.description = info['@value']
        //   }
        // })
      })
      .catch(err => console.log(err))
  }
}
</script>

<style lang="scss" scoped>
  @import "src/assets/style/artifacts/_todays-artifact";
</style>