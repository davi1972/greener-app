<template>
  <div style="margin-bottom: 60px">
    <van-nav-bar class="cr-topbar"
                 left-arrow
                 title="Events"
                 @click-left="returnBack"
    />
    <div style="width: 100%">
      <van-list
          v-model="loading"
          :finished="finished"
          finished-text="No more events"
          loading-text="Loading..."
          @load="onLoad"
          style="width: 100%"
      >
        <van-cell v-for="(item,key) in list"
                  :key="item._id"
                  right-icon
                  size="large"
                  @click="viewQuestion(item._id)">
          <template #title>
            {{ item.name }}
          </template>
          <template #label>
            <p class="event-desc">{{ item.details }}</p>
          </template>
          <template #right-icon>
            <van-rate v-model="list[key].score" readonly size="small" style="margin-top: 5px; margin-left: 5px;"/>
          </template>
        </van-cell>
      </van-list>
    </div>
  </div>
</template>

<script>
import store from "../../main";
export default {
  data() {
    return {
      list: [],
      loading: false,
      finished: false,
      type: this.$route.params.type
    };
  },
  methods: {
    returnBack() {
      this.$router.go(-1);
    },
    onLoad() {
      this.$axios({
        method: 'post',
        url: '/greener-ml/get-user-details',
        data: {
          "id": store.username
        },
        withCredentials: false
      }).then(response => {
        console.log(response)
        let liked = Object.values(response.data.likedEvents)
        let attend = Object.values(response.data.attendedEvents)
        if (this.type === "like") {
          this.list = liked
        } else this.list = attend
        this.list.forEach(item => item.score = item.score * 5)
        this.finished = true;
      })
    },
    viewQuestion(id) {
      this.$router.push({path: '/events/view/' + id});
      console.log(id)
    }
  },
  mounted() {
    console.log(this.type)
  }
}
</script>

<style scoped>
.van-nav-bar__title.van-ellipsis {
  font-size: 20px;
  font-weight: 200;
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
}

.van-nav-bar__arrow {
  font-size: 25px;
}

.van-cell__title {
  text-align: left;
  font-size: 18px;
  font-weight: 200;
  width: 100%;
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
}

.event-desc {
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
  margin: 0 5px;
  font-size: 12px;
}
</style>
