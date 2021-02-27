<template>
  <v-app id="app">
    <v-container>
      <v-row align="center" wrap>
        <v-col lg="2">
          <v-btn small color="primary">hello</v-btn>
        </v-col>
      </v-row>
    </v-container>
    <HelloWorld msg="Welcome!!"/>
  </v-app>
</template>

<script>
import HelloWorld from './components/HelloWorld.vue'

export default {
  name: 'App',
  components: {
    HelloWorld
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
