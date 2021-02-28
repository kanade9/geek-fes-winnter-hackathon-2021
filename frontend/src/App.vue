<template>
    <v-app>
      <Top />
    </v-app>
</template>

<script>
import Top from "./components/Top.vue";

export default {
  name: "App",
  components: {
    Top,
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  /* margin-top: 60px; */
  background-image: url("~@/assets/pg3.png");
  height: 100%;
}
</style>
