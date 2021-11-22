<template>
  <div class="museum-modal">
    <div class="museum-modal-wrap">
      <div>
        <span class="museum-name">{{ museumInfo.fclty_name }} </span>
        <span> [{{ museumInfo.fclty_type }}]</span>
      </div>

      <br>

      <div>{{ museumInfo.introduction }}</div>

      <br>

      <div>{{ museumInfo.address }}</div>

      <br>
      
      <div>{{ museumInfo.hompage }}</div>

      <br>

      <div class="semi-title">운영 정보</div>

      <div>
        <div class="inblock-box">평일</div>
        {{ museumInfo.weekday_open }} ~
        {{ museumInfo.weekday_close }}
      </div>

      <div>
        <div class="inblock-box">공휴일</div>
        {{ museumInfo.holiday_open }} ~
        {{ museumInfo.holiday_close }}
      </div>

      <div class="closed-date-wrap">
        <div class="inblock-box">휴무</div>
        <div class="closed-date">{{ museumInfo.closed_date }}</div>
      </div>

      <br>

      <div class="semi-title">요금 정보</div>
      <div>
        <div class="inblock-box">성인</div>
        {{ museumInfo.adult_chrg }} 원
      </div>
      <div>
        <div class="inblock-box">청소년</div>
        {{ museumInfo.student_chrg }} 원
      </div>
      <div>
        <div class="inblock-box">유아</div>
        {{ museumInfo.child_chrg }} 원
      </div>

      <div id="map" class="kakao-map"></div>
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
    initMap() {
      var mapContainer = document.getElementById('map'),
          mapOption = {
              center: new window.kakao.maps.LatLng(33.450701, 126.570667),
              level: 3
          };  
      var map = new window.kakao.maps.Map(mapContainer, mapOption);
      var geocoder = new window.kakao.maps.services.Geocoder();

      // 주소로 좌표 검색
      // geocoder.addressSearch('서울특별시 용산구 서빙고로 137' , function(result, status) {
      geocoder.addressSearch(this.museumInfo.address , function(result, status) {

          // 정상적으로 검색이 완료됐으면 
          if (status === window.kakao.maps.services.Status.OK) {

              var coords = new window.kakao.maps.LatLng(result[0].y, result[0].x);

              // 마커로 표시
              var marker = new window.kakao.maps.Marker({
                  map: map,
                  position: coords
              });

              // 지도의 중심을 결과값으로 받은 위치로 이동
              map.setCenter(coords);
          } 
      });  
    }
  },
  computed: {
    ...mapState({
      museumInfo: state => state.artifacts.museumInfo
    }),
  },
  created() {
  },
  updated() {
    if (window.kakao && window.kakao.maps) {
      this.initMap()
    } else {
      const script = document.createElement('script')
      script.onload = () => window.kakao.maps.load(this.initMap);
      script.src = 'http://dapi.kakao.com/v2/maps/sdk.js?autoload=false&appkey=ac9d810283d93186609b852e5cc33be8'
      document.head.appendChild(script)
    }
  }
}

</script>

<style lang="scss" scoped>
  @import "src/assets/style/artifacts/museum.scss";
</style>
