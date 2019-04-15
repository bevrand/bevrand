<template>
  <div id="app">

    <router-view></router-view>
  </div>
</template>


<script>
  //import your components here
  export default {

    components: {
    },

    created() {
      this.$store.commit('getTokenFromStorage')
    }
  }

</script>

<style lang="css">
  @import "./assets/css/main.css";

  .swal-button {
    background-color: #ff9500;
    color: #fff;
    border: none;
    box-shadow: none;
    border-radius: 5px;
    font-weight: 600;
    font-size: 14px;
    padding: 10px 24px;
    margin: 0;
    cursor: pointer;
  }

</style>
