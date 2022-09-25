<template>
  <div style="margin-bottom: 70px">
    <b-container>
      <van-list
          v-model="loading"
          :finished="finished"
          finished-text="No more events"
          loading-text="Loading..."
          @load="onLoad"
      >
        <b-row>
          <b-col cols="6" lg="6" md="6"
                 no-gutters="true"
                 sm="6">
            <b-row>
              <b-col v-for="(item, key) in eventList" v-bind:key="key" cols="12" lg="6" md="12"
                     no-gutters="true"
                     sm="12"
                     v-bind:style="{'padding': '0px', 'margin': '0px'}"
                     xl="6">
                <div class="cr-van-card">
                  <img :src="item.imgUrl" style="width: 100%">
                  <div>{{ item.name }}</div>
                  <p class="event-desc">{{ item.desc }}</p>
                  <van-button block color="#8ba38d"
                              text="More"
                              @click="viewQuestions(item.id)"
                  />
                </div>
              </b-col>
            </b-row>
          </b-col>
          <b-col cols="6" lg="6" md="6"
                 no-gutters="true"
                 sm="6">
            <b-row>
              <b-col v-for="(item, key) in eventList2" v-bind:key="key" cols="12" lg="6" md="12"
                     no-gutters="true"
                     sm="12"
                     v-bind:style="{'padding': '0px', 'margin': '0px'}"
                     xl="6">
                <div class="cr-van-card">
                  <img :src="item.imgUrl" style="width: 100%">
                  <div>{{ item.name }}</div>
                  <p class="event-desc">{{ item.desc }}</p>
                  <van-button block color="#8ba38d"
                              text="More"
                              @click="viewQuestions(item.id)"
                  />
                </div>
              </b-col>
            </b-row>
          </b-col>
        </b-row>
      </van-list>
    </b-container>
  </div>
</template>

<script>
import store from "../../main";
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
      eventList: [],
      eventList2: [],
      loading: false,
      finished: false,
      maxEventNum: 0,
      username: ""
    };
  },
  mounted() {
    if (!store.login) {
      router.push("/login")
    } else {
      this.username = store.username
    }
  },
  methods: {
    viewQuestions(id) {
      this.$router.push({path: '/events/view/' + id});
    },
    onLoad() {
      let num = 10
      if (this.eventList.length + this.eventList2.length > 0 && this.eventList.length + this.eventList2.length + num > this.maxEventNum) {
        num = this.maxEventNum - this.eventList.length - this.eventList2.length
      }
      console.log(num)
      console.log(this.username)
      console.log(this.eventList.length + this.eventList2.length)
      this.$axios({
        method: 'post',
        url: '/greener-ml/get-event-recommendation',
        data: {
          "userid": this.username,
          "numEvent": num,
          "offset": this.eventList.length + this.eventList2.length
        },
        withCredentials: false
      }).then(response => {
        console.log(this.$axios.data)
        console.log(response)
        this.maxEventNum = response.data.numEvents
        let events = response.data.recommendations
        for (let idx in events) {
          let e = events[idx]
          let front_event = {
            "name": e.name,
            "rating": e.score * 5,
            "id": e._id,
            "desc": e.details,
            "date": e.date,
            "time": e.time,
            "host": e.host,
            "location": e.location,
            "imgUrl": this.imageList[Math.floor(Math.random() * 6)]
          }
          if (idx % 2 === 0) {
            this.eventList.push(front_event)
          } else {
            this.eventList2.push(front_event)
          }
        }
        if (this.eventList.length + this.eventList2.length >= this.maxEventNum) {
          console.log(this.maxEventNum)
          this.loading = false;
          this.finished = true;
        } else {
          this.onLoad()
        }
      })
    }
  }
};
</script>

<style scoped>
.card-img {
  max-width: 100%;
  min-height: 100%;
  display: block;
}

.event-desc {
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
  margin: 0 5px;
  font-size: 12px;
}

.float-btn {
  width: 30%;
  font-size: 15px;
  float: left;
  margin: 5px;
}
</style>
