<template>
  <div>
    <button>
      {{value}}&nbsp;
      <img :src="icon" alt="" class="icon">
    </button>
  </div>
</template>

<script>
export default {
  name: "IconButton",
  props: ['value', 'icon']
}
</script>

<style lang="scss" scoped>
  @import "src/assets/style/artifacts/_icon-button";
</style>