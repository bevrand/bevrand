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

  .showAllButton {
    position: relative;
    display: inline-block;
    background: #ff9500;
    color: #ffffff;
    text-align: center;
    border-radius: 0.5em;
    text-decoration: none;
    padding: 0.65em 3em 0.65em 3em;
    margin-top: 2em;
    margin-bottom: 2em;
    cursor: pointer;
    outline: 0;
    font-weight: 400;
    font-size: 1em;
    font-family: "Ubuntu", sans-serif;
    -moz-transition: background-color 0.35s ease-in-out, color 0.35s ease-in-out,
    border-bottom-color 0.35s ease-in-out;
    -webkit-transition: background-color 0.35s ease-in-out,
    color 0.35s ease-in-out, border-bottom-color 0.35s ease-in-out;
    -ms-transition: background-color 0.35s ease-in-out, color 0.35s ease-in-out,
    border-bottom-color 0.35s ease-in-out;
    transition: background-color 0.35s ease-in-out, color 0.35s ease-in-out,
    border-bottom-color 0.35s ease-in-out;
  }

  .showAllButton:hover {
    color: #fff;
    background: #7A2F9E;
    letter-spacing: 1px;
    -webkit-box-shadow: 0px 5px 40px -10px rgba(0, 0, 0, 0.57);
    -moz-box-shadow: 0px 5px 40px -10px rgba(0, 0, 0, 0.57);
    box-shadow: 5px 40px -10px rgba(0, 0, 0, 0.57);
    transition: all 0.4s ease 0s;
  }

</style>
