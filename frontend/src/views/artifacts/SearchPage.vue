<template>
  <div>
    <div class="router-wrap">
      <router-link to="/search" class="router-button">
        <Button value="검색어로 찾기"></Button>
      </router-link>
      <router-link to="/search/filter" class="router-button">
        <Button value="카테고리 선택하기"></Button>
      </router-link>
    </div>
    <router-view></router-view>
  </div>
</template>

<script>
import Button from "@/components/common/Button";
  export default {
    name: "SearchPage",
    components: {
      Button
    }
  }
</script>

<style lang="scss" scoped>
    @import "src/assets/style/artifacts/_search-page.scss";

</style>e