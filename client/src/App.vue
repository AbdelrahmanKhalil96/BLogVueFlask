<template>
  <div class="vue-tempalte">
    <!-- Navigation -->
    <nav
      class="navbar shadow bg-white rounded justify-content-between flex-nowrap flex-row fixed-top"
    >
      <div class="container">
        <ul class="nav navbar-nav flex-row float-right">
          <li class="nav-item">
            <router-link class="navbar-brand float-left" to="/"
              >Home</router-link
            >
          </li>
          <li class="nav-item" v-if="loggedIn">
            <router-link class="navbar-brand float-left" to="/account"
              >Account</router-link
            >
          </li>
          <li class="nav-item">
            <router-link class="navbar-brand float-left" to="/about"
              >About</router-link
            >
          </li>
          <li class="nav-item">
            <router-link class="nav-link pr-3" to="/login">Sign in</router-link>
          </li>
          <li class="nav-item">
            <router-link class="btn btn-outline-primary" to="/"
              >Sign up</router-link
            >
          </li>
        </ul>
      </div>
    </nav>

    <div id="app">
      <router-view />
      <!--  <img alt="Vue logo" src="./assets/logo.png" /> -->
    </div>
  </div>
</template>

<script>
/*
import axios from "axios";

export default {
  data: function () {
    return {
      loggedIn: false,
    };
  },
  created() {
    axios
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
          this.loggedIn = res.data.Logged_in;
          console.log(res.data);
        }

        //this.$cookie.set("Login-Token", res.data.token);
      })
      .catch(function (error) {
        if (error.response) {
          console.log(error.response.status);
          console.log(error.response.headers);
        }
      });
  },
};*/
</script>

<style>
</style>
