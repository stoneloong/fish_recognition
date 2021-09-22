<template>
  <div id="Header">
      <h1>{{ msg }}</h1>
  </div>
</template>
<script>
export default {
  name: "Header",
  data() {
    return {
      msg: "海洋鱼类识别系统",
      activeIndex: "1",
    };
  },
};
</script>
<style scoped>
#Header {
  width: 100% auto;
  margin: 0 auto;
}
#word {
  line-height: 3.2em;
  text-align:center;
}

h1 {
  text-align: center;
  color:blueviolet;
  letter-spacing: 30px;
  font-size: 2.3em;
}

.el-menu-demo {
  width: 80%;
  margin: 0px auto;
  padding: 0px auto;
}

.top-left-edition span i {
  float: left;
  margin-right: 10px;
}

i,
input,
label {
  vertical-align: middle;
}

i {
  border: 0;
  display: block;
  cursor: pointer;
}

.top-left-edition span {
  float: left;
  font-size: 16px;
  color: #999999;
  line-height: 24px;
  margin-right: 40px;
}
</style>


