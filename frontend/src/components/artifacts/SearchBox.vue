<template>
  <div>

    <input type="text" class="search-box" :placeholder="placeholder" v-model="indexWord" @keydown.enter="searchKeyWord()"/>

    <hr>

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
import axios from 'axios'
import SearchCard from './SearchCard.vue'

  export default {
    name:'SearchBox',
    components: {
      SearchCard,
    },
    data: function() {
      return {
        //setting values
        serviceKey: 'DLuSbLjmCJIDKmhoSB7ELx3eVXXxg9ZBqh9oC8/eFWTcq2gDMqfQA7jrooSkvzWgYv/pd9a6fUJKG40K3VQXHg==',
        placeholder: '검색어를 입력해주세요.',

        // index case
        indexWord: '', //나중에 네임으로 바꾸자
        totalPage: 0,
        totalNum: 0,
        nowPage: 1,
        search_list : [],

        // infinite scroll
        // loading : false, //로딩 그게 돌아야한다면
        reminderFlag: 0,
        nextNumReminder: 0,
        nextNum: 0,
        items: []
      }
    },
    methods: {

      // 특정 유물정보 가져오기
      getArtifactPageList (pageNum) {
        axios({
              method: 'get',
              url : `/openapi/relic/list?serviceKey=${this.serviceKey}&name=${this.indexWord}&numOfRows=100&pageNo=${pageNum}`, 
            })
            .then((res) => {
              this.search_list.push(...res.data.list)
            })
      },

      // search of name
      searchKeyWord: function() {
        // 글자수 제한
        if (this.indexWord.length <2) {
          this.indexWord = ''
          this.placeholder = '2글자 이상 입력해주세요'
          return false
        } 

        // 검색결과 초기화
        this.search_list = []
        this.items = []

        // 응답 요청
        axios({
          method: 'get',
          url : `/openapi/relic/list?serviceKey=${this.serviceKey}&name=${this.indexWord}&numOfRows=100&pageNo=1`, 
        })
        .then((res) => {
          console.log(res)
          if (res.data.totalCount === 0) {
            this.indexWord = ''
            this.placeholder = '결과가 없습니다'
            return false
          }
          this.nextNum = 0
          this.totalNum = res.data.totalCount
          this.totalPage = parseInt(res.data.totalCount /100) + 2
          this.search_list.push(...res.data.list)
          this.nowPage = this.nowPage + 1
          this.indexWord = ''
          this.placeholder = ''
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
          // console.log(err)
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
  @import "src/assets/style/artifacts/_search-box.scss";
</style>

