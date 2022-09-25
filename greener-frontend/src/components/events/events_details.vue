<template>
  <div style="margin-bottom: 70px">
    <van-nav-bar class="cr-topbar"
                 :title="questionName"
                 left-arrow
                 fixed placeholder
                 @click-left="returnBack"
    />
    <b-container>
      <b-row>
        <b-col cols="12" lg="6" xl="6" sm="12" md="12"
               no-gutters="true"
               v-bind:style="{'padding': '0px'}">
          <div class="cr-van-card">
            <img v-for="(item, key) in imgUrl" v-bind:key="key" :src="item" style="width: 100%; height: 100%">
            <van-divider dashed>Events Description</van-divider>
            <div class="cr-desc">
              {{ this.questionContent }}
            </div>
            <ul style="text-align: left; margin: 10px; line-height: 30px">
              <li>
                <van-icon name="location-o"/>
                Location: {{ this.location }}
              </li>
              <li>
                <van-icon name="wap-home-o"/>
                Host: {{ this.host }}
              </li>
              <li>
                <van-icon name="flag-o"/>
                Link: <a style="color: #8ba38d" :href="this.link">click</a></li>
              <li>
                <van-icon name="star-o"/>
                Recommendation Count: {{ this.recommendCount }}
              </li>
              <li>
                <van-icon name="like-o"/>
                People Responded: {{ this.pplResp }}
              </li>
              <li>
                <van-icon name="bookmark-o"/>
                Tags: <span v-for="(item, key) in tags" v-bind:key="key">
              <van-tag color="#8ba38d">{{ item }}</van-tag><span style="color: #fff">-</span></span></li>
            </ul>
            <van-loading type="spinner" size="24px" style="margin: 20px" v-show="this.loading" />
            <van-button round type="info"
                        @click="submitAttend(questionId)"
                        color="#8ba38d"
                        style="font-size: 20px; margin: 10px">Attend
            </van-button>
            <van-button round type="info"
                        @click="submitLike(questionId)"
                        color="#8ba38d"
                        style="font-size: 20px; margin: 10px">Like
            </van-button>
          </div>
        </b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script>
import store from "@/main";
import router from "@/router";

export default {
  data() {
    return {
      imageList: [
        require("@/assets/ds-hash.png"),
        require("@/assets/ds-queue.png"),
        require("@/assets/ml.png"),
        require("@/assets/ag-rec.png"),
        require("@/assets/ds-array.png"),
        require("@/assets/ds-bst.png")
      ],
      questionId: this.$route.params.id,
      questionName: "Events " + this.$route.params.id,
      questionContent: "",
      rating: 0,
      difficulty: 0,
      comment: '',
      imgUrl: [],
      link: "",
      host: "",
      location: "",
      recommendCount: 0,
      pplResp: "",
      tags: [],
      loading: false
    }
  },
  mounted() {
    console.log(store.login)
    this.$axios({
      method: 'post',
      url: '/default/get-event-detail',
      data: {
        "id": this.questionId
      },
      withCredentials: false
    }).then(response => {
      console.log(response)
      this.questionName = response.data.name
      this.questionContent = response.data.details
      this.imgUrl = [this.imageList[Math.floor(Math.random() * 6)]]
      this.location = response.data.location
      this.link = response.data.link
      this.host = response.data.host
      this.recommendCount = response.data.recommendCount
      this.pplResp = response.data.numPeopleResponded
      for (let i in response.data.attributes) {
        let item = response.data.attributes[i]
        if (item === 1) {
          this.tags.push(i)
        }
      }
    })
  },
  methods: {
    returnBack() {
      router.go(-1);
    },
    submitLike(id) {
      console.log([id]);
      console.log(store.username)
      this.loading = true
      this.$axios({
        method: 'post',
        url: '/greener-ml/greener-ml-like-api',
        data: {
          "eventList": [id],
          "userid": store.username
        },
        withCredentials: false
      }).then(response => {
        console.log(response)
        this.loading = false
        this.$toast.success("Liked!");
      })
    },
    submitAttend(id) {
      console.log(id);
      console.log(store.username)
      this.loading = true
      this.$axios({
        method: 'post',
        url: '/greener-ml/greener-ml-attend-api',
        data: {
          "eventList": [id],
          "userid": store.username
        },
        withCredentials: false
      }).then(response => {
        console.log(response)
        this.loading = false
        this.$toast.success("Attend Successfully!");
      })
    }
  }
}
</script>

<style scoped>

.van-nav-bar__title.van-ellipsis {
  font-size: 20px;
  font-weight: 200;
}

.van-nav-bar__arrow {
  font-size: 25px;
}

.van-nav-bar .van-icon {
  color: rgb(134, 134, 134);
}

.van-cell__title {
  text-align: left;
  font-size: 18px;
  font-weight: 200;
}


.cr-desc {
  margin: 10px;
  text-indent: 2em;
  text-align: left;
}

.cr-sample {
  margin: 10px;
  text-align: left;
  background: #f7f9fa;
  padding: 10px;
  line-height: 25px;
  font-family: "Courier New";
  font-size: 15px;
}
</style>
