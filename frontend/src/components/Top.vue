<template>
  <div class="top">
    <v-container>
      <v-row style="padding-top:100px;">
        <v-col cols="12" lg="5" style="padding:20px">
          <v-row>
            <h1>技育祭おすすめ講演</h1>
            <br />
            <h1>レコメンダー</h1>
          </v-row>
          <v-row>
            <p style="text-align: left">
              誰の講演を聞こうかと迷っている方へ、おすすめの講演をAIによってレコメンドします。
              興味のあるワードを含んだ文章を入力してみてください！
            </p>
          </v-row>
          <v-row>
            <v-textarea counter dark outlined v-model="text"></v-textarea>
          </v-row>
          <v-row>
            <v-btn elevation="5" large color="success" @click="post_recommend()">検索する</v-btn>
          </v-row>
        </v-col>
        <v-spacer/>
        <v-col lg="6">
          <v-card
            v-for="(data, key) in random_list"
            :key="key"
            style="margin: 1rem"
            outlined
            elevetion=10
          >
            <v-card-title class="justify-center" style="font-weight: bold">
              {{ data.title }}
            </v-card-title>
            <v-card-subtitle>
              {{ data.name }}
            </v-card-subtitle>
            <span>
             {{ data.date }}
            </span>
            <br>
            {{ data.start_time }} から {{ data.end_time }} 会場:
            {{ data.hall_no }}
            <br />
            <a v-bind:href="data.twitter">{{data.twitter}}</a>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
import axios from "axios";
import dataset from '../assets/test.json'
export default {
  name: "Top",
  data() {
    return {
      text: "",
      random_list: [],
      dataset: dataset,
      list_str: '{"kw": ["フロント", "深層学習"]}',
    };
  },
  methods: {
    post_recommend: async function () {
      let text_json_str = '{"text":' + '"' + this.text + '"}';
      await axios
        .post("http://localhost/recommend", text_json_str, {
          headers: { "Content-Type": "application/json" },
        })
        .then((response) => {
          // alert(response.data);
          this.random_list = response.data;
        })
        .catch((error) => {
          alert(error);
        });
    },
    post_debug: function () {
      this.random_list = dataset;
    },
    getPic(index) {
    return '../assets/image' + index + '.jpg';
    }
  }
}
</script>

<style>
</style>
