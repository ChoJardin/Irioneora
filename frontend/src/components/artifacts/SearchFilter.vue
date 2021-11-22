<template>
  <div>

    <div id="float-clear-div">
        <p class="theme-text">{{theme}}</p>
        <div class="search-filter-wrap-div">
          <div class= "search-button" @click="buttonSwitch($event,idx)" v-for="(ele,idx) in sortlist" :key="idx">
            {{ele.name}}
          </div>
        </div>
        
      </div>

  </div>
</template>

<script>
global.jQuery = require('jquery');
var $ = global.jQuery;
window.$ = $;
  export default {
    name: 'SearchFilter',
    props: {
      theme: {
        type: String,
        required: true
      },
      startnum: {
        type: Number,
        required: true
      },
      sortlist: {
        type: Array,
        required: true
      }
    },
    data () {
      return {
        value: ''
      }
    },
    
    methods: {
      buttonSwitch: function ($event,idx) {
        this.value = this.sortlist[idx].code
        
        if ($event.target.classList[1] === "on") {
          $event.target.classList.remove("on")
          this.value = ''
          this.$emit('change', this.value)
        } else {
          var j = this.startnum
          var num = j+this.sortlist.length
          const btns = document.getElementsByClassName("search-button")
          for (j ; j < num; j++) {
            const btn = btns[j]
            $(btn).removeClass('on')
          }
          $event.target.classList.add("on")
          this.$emit('change', this.value)
        }
      return false;
      },
    },
  }
</script>

<style lang="scss" scoped>
  @import "src/assets/style/artifacts/_search-filter.scss";
</style>