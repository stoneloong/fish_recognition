<template>
  <div id="Footer">
    <p>{{ msg }}</p>
  </div>
</template>
<script>
export default {
  name: "Footer",
  data() {
    return {
      msg: "Copyright @Leon",
    };
  },
};
</script>
<style scoped>
#Footer {
  /*background:#F2F6FC;*/
  border-radius: 15px;
  width: 80% auto;
  height: 20px auto;
  margin: 0px auto;
  margin-top: 0px auto;
}

p {
  color:blueviolet;
  text-align: center;
  margin: 30px auto;
  font-size: 1.1em;
}
</style>


