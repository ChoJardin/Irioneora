<template>

  <transition name="modal">
    <div class="modal-mask">
      <div class="modal-wrapper">
        <div class="modal-container">

          <!--<div class="modal-header">-->
          <!--  <slot name="header">-->
          <!--    <button class="modal-header-button">X</button>-->
          <!--  </slot>-->
          <!--</div>-->

          <div class="modal-body">
            <slot name="body">
              {{error}}
            </slot>
          </div>

          <div class="modal-footer">
            <slot name="footer">
              <button class="modal-default-button" @click="$emit('close')">
                닫기
              </button>
            </slot>
          </div>
        </div>
      </div>
    </div>
  </transition>

</template>

<script>
export default {
  name: "ErrorModal",
  props: ['error']
}
</script>

<style lang="scss" scoped>
  @import "src/assets/style/artifacts/_error-modal.scss";
</style>