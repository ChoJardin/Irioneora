<template>
  <div class="component">
    <!--
    컴포넌트 사용법
    부모 컴포넌트에서 props로 id, label, type, placeholder, error를 보냅니다.
    -> id 는 필수 입력!!
    -> 적지 않을 경우,
      label과 placeholder는 '', type === text
      error === false -> 이거 보내주면 빨간 효과 발생
    부모 컴포넌트에서 :input.sync="{연결하고 싶은 data이름}" 이렇게하면,
    v-model로 {연결하고 싶은 data이름} 이거 연결한 거랑 동일하게 사용가능
    eventListner를 추가하고 싶은 경우 아래의 method 추가해서 그걸 들으면 되요
    -->
    <div class="wrap">
        <label v-html="label" :for="id"></label>
        <input
            v-model="input"
            :id="id"
            :type="type"
            :placeholder="placeholder"
            :class="{error: !!error}"
            @input="onType($event)"
            @keypress.enter="onEnter($event)"
            @focus="onFocus($event)"
        >

      <!--에러메세지-->
      <div v-if="!!error" class="error-message">
        {{error}}
      </div>

    </div>
  </div>
</template>

<script>
export default {
  name: "UserInput",
  props: {
    id: {
      type: String,
      default: 'input',
      required: true
    },
    label: {
      type: String,
      default: ''
    },
    placeholder: {
      type: String,
      default: ''
    },
    type: {
      type: String,
      default: 'text'
    },
    error: {
      type: [Boolean, String],
      default: ''
    },
  },
  data() {
    return {
      input: '',
    }
  },
  methods: {
    onType() {
      this.$emit('update:input', this.input)
    },
    // enter 입력 -> @keyup-enter
    onEnter() {
      this.$emit('keyup-enter')
    },
    //focus -> @on-focus
    onFocus() {
      this.$emit('on-focus')
    },
    //값 초기화
    //부모에서 자식 input 초기화시 사용
    onReset() {
      this.input = ''
    }
  },
}
</script>

<style scoped>
.component {
  display: flex;
  justify-content: center;
  height: 50px;
  margin-bottom: 25px;
}

.wrap {
  position: relative;
  display: flex;
  flex-direction: column;
  justify-content: center;
  width: 100%;
}

label {
  position: relative;
  margin-left: 15px;
  font-size: 0.8em;
  width: 60px;
  display: flex;
  justify-content: center;
  text-align: center;
  z-index: 1;
  color: #DEC8A4;
}

input{
  border: none;
  outline:none;
  display:inline-block;
  height:50px;
  vertical-align:middle;
  position: absolute;
  /*border-radius:25px;*/
  width:100%;
  box-sizing:border-box;
  padding:0 0 0 80px;
  /*box-shadow: 0 0 15px -9px rgba(0, 0, 0, 0.55);*/
  font-size: 0.9em;
  font-family: 'Noto Serif KR';
  background: #081420;
  color: #DEC8A4;

}

input:focus {
  border-bottom: 1px solid rgba(222, 200, 164, 0.5);
}

input.error {
  border-bottom: 1px solid #cd4e3e;
}

.error-message {
  position: absolute;
  color: #cd4e3e;
  margin-top: 74px;
  margin-left: 20px;
  font-size: 0.8em;
}

</style>