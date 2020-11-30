
/* eslint-disable */ 
<template>
  <div class="vertical-center">
    <h1 class="inner-block">Latest Posts</h1>
    <!-- Create -->
    <hr />
    <p class="error" v-if="error">{{ error }}</p>
    <div
      class="inner-block"
      v-for="(post, index) in posts"
      v-bind:item="post"
      v-bind:index="index"
      v-bind:key="post.id"
    >
      <h3 class="mb-0">{{ post.title }}</h3>
      <div class="mb-1 text-muted">{{ post.date_posted }}</div>
      <p class="card-text mb-auto">{{ post.content }}</p>
      <a href="#">Continue reading</a>
    </div>
  </div>
</template>

<script>
//import axios from "axios";
import PostService from "../PostService";
export default {
  name: "PostComponent",
  data() {
    return {
      posts: [],
      Author: "",
      content: "",
      title: "",
      date_posted: "",
      error: "",
      text: "",
      loggedIn: false,
    };
  },
  async created() {
    try {
      /*   console.log(document.cookie.split(":")[1]);
      console.log(document.cookie.split(":")[1]);
      console.log(document.cookie.split(":")[1]);*/
      /*    axios
        .get("http://localhost:5000/checkUser", {
          headers: {
            "x-access-token": document.cookie.split(":")[1],
          },
        })
        .then((res) => {
          if (res.Error) {
            this.error("You Need To Log in First");
            console.log(res.data);
          } else {
            console.log(res.data);
            this.loggedIn = res.data;
            console.log(res.data);
          }

          //this.$cookie.set("Login-Token", res.data.token);
        })
        .catch(function (error) {
          if (error.response) {
            console.log(error.response.status);
            console.log(error.response.headers);
          }
        });*/
      this.posts = await PostService.getPosts();
    } catch (err) {
      this.error = err.message;
    }
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
/*h3 {
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
}*/
</style>
