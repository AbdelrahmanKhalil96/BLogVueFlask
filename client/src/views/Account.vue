<template>
  <div class="vertical-center">
    <h1 class="inner-block">UserData</h1>

    <div v-if="posts">
      <div class="inner-block" v-bind:item="userData">
        <h3>{{ userData.username }}</h3>
        <h3>{{ userData.email }}</h3>
        <!-- Create -->
        <h3 v-if="userData.admin">The User Is An Admin</h3>
        <h2 style="color: red" class="error" v-if="error">{{ error }}</h2>
      </div>
      <hr />

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
    <div style="color: red" class="inner-block" v-else>
      You Need To Be Logged In To Access Your Account
    </div>
  </div>
</template>

<script>
/* eslint-disable */

import axios from "axios";

// @ is an alias to /src
export default {
  data() {
    return {
      posts: [],
      userData: [],
      error: "",
    };
  },
  async created() {
    //const postData = { username: this.userName, password: this.password };
    var posts = this.posts;
    var userData = this.userData;
    try {
      axios
        .get("http://localhost:5000/account", {
          headers: {
            "x-access-token": document.cookie.split(":")[1],
          },
        })
        .then((res) => {
          if (res.Error) {
            this.error("You Need To Log in First");
          } else {
            this.posts = res.data.User_Posts;
            this.userData = res.data.User_Data;
          }

          //this.$cookie.set("Login-Token", res.data.token);
        })
        .catch((error) => {
          console.log("Error on Authentication");
          this.error = error;
          console.log(error);
        });
    } catch (err) {
      console.log("Invalid UserName Or PassWord");
      this.error = err.message;
    }
  },
};
</script>
