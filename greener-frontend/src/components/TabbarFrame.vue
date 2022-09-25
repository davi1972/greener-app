<template>
  <div>
    <router-view/>
    <van-popup closeable v-model="showMsg" round position="top" :style="{ height: '70px' }">
      <div class="pop-message">{{ this.message }}</div>
    </van-popup>
    <van-popup closeable v-model="showPop" round position="top" :style="{ height: '90%' }">
      <div class="pop-message">
        <van-cell-group inset>
          <van-field
              v-model="eventName"
              :rules="[{ required: true, message: 'Please fill event name' }]"
              label="Event Name"
              name="Event Name"
              placeholder="Event Name"
          />
          <van-field
              v-model="eventDesc"
              :rules="[{ required: true, message: 'Please fill event desc' }]"
              label="Event Details"
              name="Event Details"
              placeholder="Event Desc"
          />
          <van-field
              v-model="host"
              :rules="[{ required: true, message: 'Please fill event desc' }]"
              label="Host"
              name="Host"
              placeholder="Host"
          />
          <van-field
              v-model="location"
              :rules="[{ required: true, message: 'Please fill event desc' }]"
              label="Location"
              name="Location"
              placeholder="Location"
          />
          <van-field
              v-model="link"
              :rules="[{ required: true, message: 'Please fill event desc' }]"
              label="Link"
              name="Link"
              placeholder="Link"
          />
          <b-row>
            <b-col cols="4" lg="4" md="4" v-for="(a, k) in attrs" :key="k">
              <van-button block :plain="!a.selected" color="#8ba38d" @click="addAttr(a)" class="cr-van-card"
                          size="small">
                {{ a.name }}
              </van-button>
            </b-col>
          </b-row>
        </van-cell-group>
        <div class="cr-van-card">
          <van-loading type="spinner" size="24px" style="margin: 20px" v-show="this.loading" />
          <van-button block color="#8ba38d" @click="submit()">
            Submit
          </van-button>
        </div>
      </div>
    </van-popup>
    <van-tabbar route active-color="#afbc90" inactive-color="#7f8182">
      <van-tabbar-item replace icon="add-o" @click="showPopup">New</van-tabbar-item>
      <van-tabbar-item replace to="/events" icon="fire-o">Recommendations</van-tabbar-item>
      <!--      <van-tabbar-item replace to="/matching" icon="star-o">Match</van-tabbar-item>-->
      <van-tabbar-item replace to="/" icon="user-circle-o">Me</van-tabbar-item>
    </van-tabbar>
  </div>
</template>

<script>
export default {
  data() {
    return {
      msgNum: 0,
      showPop: false,
      showMsg: false,
      message: 'Upload Successfully',
      eventName: '',
      eventDesc: '',
      host: '',
      link: '',
      location: '',
      attrs: [
        {name: "community", selected: false},
        {name: "environment", selected: false},
        {name: "food", selected: false},
        {name: "physical", selected: false},
        {name: "virtual", selected: false}
      ],
      loading: false
    };
  },
  methods: {
    showPopup() {
      this.showPop = true
    },
    submit() {
      this.loading = true
      let payload = {
        "attributes": {
          "community": this.attrs[0].selected ? 1 : 0,
          "environment": this.attrs[1].selected ? 1 : 0,
          "food": this.attrs[2].selected ? 1 : 0,
          "physical": this.attrs[3].selected ? 1 : 0,
          "virtual": this.attrs[4].selected ? 1 : 0
        },
        "details": this.eventDesc,
        "host": this.host,
        "link": this.link,
        "location": this.location,
        "name": this.eventName
      }
      console.log(payload)
      this.$axios({
        method: 'post',
        url: '/default/add-new-event-sequence',
        data: {
          "payload": payload
        },
        withCredentials: false
      }).then(response => {
        console.log(response)
        this.loading = false
        this.showPop = false
        this.showMsg = true
      })
    },
    addAttr(item) {
      console.log(item)
      item.selected = !item.selected
    }
  }
};
</script>

<style>
.van-tabbar--fixed {
  height: 60px;
  border: solid 1px #7a857b;
  border-top-left-radius: 30px;
  border-top-right-radius: 30px;
}

.van-nav-bar .van-icon {
  color: #8ba38d;
}

.van-nav-bar--fixed {
  border: solid 1px #7a857b;
  border-bottom-left-radius: 30px;
  border-bottom-right-radius: 30px;
}

.van-nav-bar {
  border: solid 1px #7a857b;
  border-bottom-left-radius: 30px;
  border-bottom-right-radius: 30px;
}

.van-tabbar-item__icon {
  font-size: 25px;
}

.cr-van-card {
  margin: 10px;
  border-radius: 15px;
  overflow: hidden;
  border: solid #8ba38d;
}

.pop-message {
  margin: 20px;
  font-size: 16px;
  color: #969799;
  font-weight: 400;
}

</style>
