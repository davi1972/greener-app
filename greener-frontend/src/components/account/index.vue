<template style="height: 100%">
  <div v-bind:style="{backgroundImage:'url(' + bgImg + ')',
                        backgroundRepeat:'no-repeat',
                        height: '100vh',
                        lineHeight: '100vh',
                        backgroundSize:'cover'}">
    <div class="cr-van-card login-card">
          <div class="logo-box"
               v-bind:style="{backgroundImage:'url(' + logo + ')',
             backgroundRepeat:'no-repeat',
             backgroundSize:'100% 100%'}">
          </div>
      <van-form>
        <van-cell-group inset>
          <van-field
              v-model="username"
              :rules="[{ required: true, message: 'Please fill user name' }]"
              label="User Name"
              name="User Name"
              placeholder="User Name"
          />
          <van-field
              v-model="password"
              :rules="[{ required: true, message: 'Please fill password' }]"
              label="Password"
              name="Password"
              placeholder="Password"
              type="password"
          />
        </van-cell-group>
        <b-row v-bind:style="{margin: 0}">
          <b-col cols="6" lg="6" md="6" no-gutters="true" sm="6">
            <div style="margin: 6px;">
              <van-button block color="#8ba38d" round  @click="onSubmit">
                Log In
              </van-button>
            </div>
          </b-col>
          <b-col cols="6" lg="6" md="6" no-gutters="true" sm="6">
            <div style="margin: 6px;">
              <van-button block round @click="onRegistration">
                Sign Up
              </van-button>
            </div>
          </b-col>
        </b-row>
      </van-form>
    </div>
  </div>
</template>


<script>
import router from "@/router";
import store from "../../main"

export default {
  data() {
    return {
      bgImg: require("@/assets/bg.jpg"),
      logo: require("@/assets/logo.png"),
      username: '',
      email: '',
      password: '',
    };
  },
  mounted() {
    store.login = false
    console.log(store)
  },
  methods: {
    onSubmit() {
      console.log(this.username, this.password)
      this.$toast("Loading...")
      this.$axios({
        method: 'post',
        url: '/default/user-login-sequence',
        data: {
          "username": this.username,
          "password": this.password
        },
        withCredentials: false
      }).then(response => {
        console.log(response)
        if (response.data.message === "Login successful") {
          this.$toast.success("Welcome! " + this.username)
          store.login = true
          store.username = this.username
          router.push("/")
        } else {
          this.$toast.fail(response.data.message)
        }
      })
    },
    onRegistration() {
      console.log(this.username, this.password)
      this.$toast("Loading...")
      this.$axios({
        method: 'post',
        url: '/default/user-registration-sequence',
        data: {
          "username": this.username,
          "password": this.password
        },
        withCredentials: false
      }).then(response => {
        console.log(response)
        if (response.data.success !== undefined) {
          this.$toast.success(this.username + " registered successfully");
          router.push("/login")
        } else {
          this.$toast.fail(response.data.message)
        }
      })
    }
  }
};
</script>


<style scoped>
.login-card {
  background: white;
  display:inline-block;
}

.logo-box {
  width: 200px;
  height: 70px;
  overflow: hidden;
  margin: 20px auto;
}
</style>
