<template>
  <div class="top">
    <v-container>
      <v-row style="padding-top:100px;">
        <v-col lg="5">
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
          >
            <v-card-title class="justify-center" style="font-weight: bold">
              {{ data.title }}
            </v-card-title>
            <img src='../assets/image/0.jpg'>
            <v-card-subtitle>
              {{ data.name }}
            </v-card-subtitle>
            <br />
            {{ data.start_time }} から {{ data.end_time }} 会場:
            {{ data.hall_no }}
            <br />
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
        .post("http://gpu.hongo.wide.ad.jp:5000/recommend", text_json_str, {
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
    get_random: async function () {
      await axios
        .get("http://gpu.hongo.wide.ad.jp:5000/")
        .then((response) => {
          alert(response.statusText);
        })
        .catch((error) => {
          alert(error);
        });
    },
  },
};
</script>

<style>
</style>
