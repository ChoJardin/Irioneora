<template>
  <div class="museum-modal">
    <div>
      <span>
        {{ museumInfo.fclty_name }}
      </span>
      <span>
        {{ museumInfo.fclty_type }}
      </span>
    </div>
    <div>
      {{ museumInfo.address }}
    </div>
    <div>
      {{ museumInfo.hompage }}
    </div>
    <div>
      {{ museumInfo.weekday_open }}
    </div>
    <div>
      {{ museumInfo.weekday_close }}
    </div>
    <div>
      {{ museumInfo.holiday_open }}
    </div>
    <div>
      {{ museumInfo.holiday_close }}
    </div>
    <div>
      {{ museumInfo.closed_date }}
    </div>
    <div>
      {{ museumInfo.adult_chrg }}
    </div>
    <div>
      {{ museumInfo.student_chrg }}
    </div>
    <div>
      {{ museumInfo.child_chrg }}
    </div>
    <div>
      {{ museumInfo.introduction }}
    </div>
  </div>
</template>

<script>
import {mapState} from "vuex";

export default {
  name: 'MuseumModal',
  components: {},
  props: {},
  data() {
    return {
    }
  },
  methods: {

  },
  computed: {
    ...mapState({
      museumInfo: state => state.artifacts.museumInfo
    })
  },
  created() {
  }
}

</script>

<style lang="scss" scoped>
  @import "src/assets/style/artifacts/museum.scss";
</style>
