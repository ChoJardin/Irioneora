<template>
  <div>
    <hr>
    <SearchFilter @change="getNation" id="search-filter" theme="시대 구분" :sortlist="nationalityName2" :startnum = "0"  />
    <SearchFilter @change="getPurpose" id="search-filter" theme="유물 종류" :sortlist="purposeName2" :startnum = "8"  />
    <div id="float-clear-div">
      <div class="search-button-div">
        <button class="search-button" @click="searchFilters" value="search">search</button>
      </div>
      <hr>
    </div>
    <ErrorModal v-if="isError" :error="error" @close="isError=false"></ErrorModal>


    <div class="search-wrap-div">
      <SearchCard 
        v-for="(item,idx) of items" 
        :key="idx"
        :artifact="item"
        />
    </div>

  </div>
</template>

<script>
import SearchFilter from "@/components/artifacts/SearchFilter.vue";
import axios from 'axios'
import SearchCard from '@/components/artifacts/SearchCard.vue'
import ErrorModal from "@/components/artifacts/ErrorModal";

  export default {
    name: 'SearchFilterPage',
    components : {
      SearchFilter,
      SearchCard,
      ErrorModal,
    },
    data () {
      return {
        nationalityName2:[
          {name: '청동기', num:0, code: 'PS06001004'},
          {name: '고구려', num:1, code: 'PS06001008'},
          {name: '백제', num:2, code: 'PS06001009' },
          {name: '신라', num:3, code: 'PS06001010' },
          {name: '통일신라', num:4, code: 'PS06001013' },
          {name: '고려', num:5, code: 'PS06001016' },
          {name: '조선', num:6, code: 'PS06001018' },
          {name: '광복이후', num:7, code: 'PS06001021' },
         
        ],
        purposeName2:[
          {name: '전통과학', num:3, code:'PS09006' },
          {name: '사회생활', num:2, code:'PS09007' },
          {name: '종교신앙', num:0, code:'PS09008' },
          {name: '문화예술', num:1, code:'PS09009' },
        ],

        /// SEARCH BOX
        //setting values
        serviceKey: "DLuSbLjmCJIDKmhoSB7ELx3eVXXxg9ZBqh9oC8/eFWTcq2gDMqfQA7jrooSkvzWgYv/pd9a6fUJKG40K3VQXHg==",

        // FILTER
        nationalityCode: "",
        purposeCode: "",

        // index case
        totalPage: 0,
        totalNum: 0,
        nowPage: 1,
        search_list : [],
      
        // infinite scroll
        // loading : false,
        reminderFlag: 0,
        nextNumReminder: 0,
        nextNum: 0,
        items: [],
        isError: false,
        error: '검색 필터를 설정해주세요'
      }
    },
    
    methods : {
      getNation (value) {
        this.nationalityCode = value
      },
      getPurpose (value) {
        this.purposeCode = value
      },
      getArtifactPageList (pageNum) {
        axios({
              method: 'get',
              url : `/openapi/relic/list?serviceKey=${this.serviceKey}&nationalityCode=${this.nationalityCode}&purposeCode=${this.purposeCode}&numOfRows=100&pageNo=${pageNum}`, 
            })
            .then((res) => {
              this.search_list.push(...res.data.list)
            })
      },
      searchFilters () {
        // 검색결과 초기화
        this.search_list = []
        this.items = []
      
        // 필터제한
        if (this.nationalityCode === '' && this.purposeCode === '')  {
          // 어떻게 표현하지
          this.isError = true
          return false
        } 

        // 응답 받아오기
        axios({
          method: 'get',
          url : `/openapi/relic/list?serviceKey=${this.serviceKey}&nationalityCode=${this.nationalityCode}&purposeCode=${this.purposeCode}&numOfRows=100&pageNo=1`, 
        })
        .then((res) => {
          if (res.data.totalCount === 0) {
            return false
          }
          this.nextNum = 0
          this.totalNum = res.data.totalCount
          this.totalPage = parseInt(res.data.totalCount /100) + 2
          this.search_list.push(...res.data.list)
          this.nowPage = this.nowPage + 1
        })
        .then(() => {
          for (var j = this.nextNum; j < this.nextNum+18; j++) {
            if (this.search_list[j] !== undefined) {
              this.items.push(this.search_list[j]);
            } 
          }
          this.nextNum = j
        })
        .catch((err) => {
          console.log(err)
        })
      },

      // infinite methods
      loadMore () {
        if (this.nextNum > this.totalNum) {

          return false
        }
        // this.loading = true;
        setTimeout(_ => {

          for (var i = 0; i < 6; i++) {
            this.nextNum++
            this.items.push(this.search_list[this.nextNum]);
            if (this.nextNum > this.totalNum) {

              return false
            }
          }
          // this.loading = false;
        }, 200);

        this.nextNumReminder = this.nextNum%100
    
        if (this.reminderFlag === 1 && this.nextNumReminder < 20 ) {
          this.reminderFlag = 0
        }
        
        if ( this.nextNumReminder > 70 && this.reminderFlag === 0 && this.nowPage < this.totalPage ) {
          this.getArtifactPageList(this.nowPage)
          this.nowPage = this.nowPage + 1
          this.reminderFlag = 1
        }

      },

    },

    mounted () {
      // Detect when scrolled to bottom.
      const listElm = document.querySelector('.search-wrap-div');
      listElm.addEventListener('scroll',_ => {

        if(listElm.scrollTop + listElm.clientHeight >= listElm.scrollHeight-10) {
          this.loadMore();
        }
      })
    },
  }
</script>

<style lang="scss" scoped>
  @import "src/assets/style/artifacts/_search-filterpage.scss";
</style>