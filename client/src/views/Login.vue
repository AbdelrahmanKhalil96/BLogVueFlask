<template>
  <div class="vertical-center">
    <div class="inner-block">
      <div id="Login">
        <form>
          <h3>Sign In</h3>

          <div class="form-group">
            <label>User Name</label>
            <input
              v-model="userName"
              type="text"
              class="form-control form-control-lg"
              required
            />
          </div>

          <div class="form-group">
            <label>Password</label>
            <input
              v-model="password"
              type="password"
              class="form-control form-control-lg"
              required
            />
          </div>

          <button
            @click.prevent="sendPost()"
            type="submit"
            class="btn btn-dark btn-lg btn-block"
          >
            Sign In
          </button>

          <p class="forgot-password text-right mt-2 mb-4">
            <router-link to="/forgot-password">Forgot password ?</router-link>
          </p>

          <div class="social-icons">
            <ul>
              <li>
                <a href="#"><i class="fa fa-google"></i></a>
              </li>
              <li>
                <a href="#"><i class="fa fa-facebook"></i></a>
              </li>
              <li>
                <a href="#"><i class="fa fa-twitter"></i></a>
              </li>
            </ul>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>
<script>
import axios from "axios";

export default {
  data: function () {
    return {
      userName: "",
      password: "",
    };
  },
  methods: {
    sendPost() {
      //const postData = { username: this.userName, password: this.password };
      try {
        let self = this;

        axios
          .post(
            "http://localhost:5000/login",
            {},
            {
              auth: {
                username: this.userName,
                password: this.password,
              },
            }
          )
          .catch(function (error) {
            if (error.response) {
              console.log(error.response.status);
              console.log(error.response.headers);
            }
          })
          .then((res) => {
            console.log((document.cookie = "Login_is:" + res.data.token));
            console.log(res.status);
            if (res.status == "200") {
              self.$router.push("/");
            }
            //this.$cookie.set("Login-Token", res.data.token);
          });
      } catch (err) {
        console.log("Invalid UserName Or PassWord");
      }
    },
  },
};
</script>