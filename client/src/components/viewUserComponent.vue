
/* eslint-disable */ 
<template>
  <div class="vertical-center">
    <h1 class="inner-block">User Account</h1>
    <!-- Create -->
    <hr />
    <p class="error" v-if="error">{{ error }}</p>

    <div class="inner-block">
      {{ userData.username }}
      {{ userData.email }}
      {{ userData.admin }}
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
  </div>
</template>

<script>
import UserService from "../userService";
export default {
  name: "viewUserComponent",
  data() {
    return {
      posts: [],
      Author: "",
      content: "",
      title: "",
      date_posted: "",
      error: "",
      public_id: "",
      userData: [],
    };
  },
  async created() {
    try {
      this.posts = await UserService.getUser().User_Posts;
      this.userData = await UserService.getUser().User_Data;
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
