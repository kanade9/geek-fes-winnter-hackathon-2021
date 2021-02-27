<template>
  <div class="top">
    <h1> 技育祭おすすめ講演レコメンダー</h1>
    <h3 style='padding: 3rem;'> このボタンを押すとおすすめの講演を表示します </h3>
    <v-btn small color="primary" @click="post_random()">ランダムに表示する</v-btn>
    <h2 style='padding: 4rem;'>あなたにおすすめの講演はこれだ！！</h2>
    <v-container>
      <v-row align="center" wrap>
        <v-col lg="4">
        </v-col>
      </v-row>
      <v-row>
        <v-col lg="4">
          <div v-for="(text,key) in random_list" :key="key">
            {{ text }}
          </div>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'Top',
  data() {
    return{
     random_list: []
    }
  },
  props: {
    msg: String
  },
  methods: {
    post_random: async function () {
      await axios.post('http://localhost:80/random', JSON.stringify('{"kw": ["フロント", "深層学習"]}'), {
        headers: {"Content-Type": "application/json"}
      })
      .then(response => {
        alert(response.statusText);
        })
      .catch(error => {
        alert(error);
        })
      },
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
