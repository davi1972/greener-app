<template>
  <div style="margin-bottom: 70px">
    <b-container style="padding: 0">
      <van-tabs swipeable animated>
        <van-tab v-for="(img, key) in imageList" v-bind:key="key">
          <b-row style="padding: 15px">
            <b-col cols="12" lg="4" md="12"
                   no-gutters="true"
                   sm="12"
                   v-bind:style="{'padding': '0px', 'margin': '0px'}"
                   xl="4">
              <div class="cr-van-card">
              <img :src="img" style="width: 100%">
              <van-goods-action-button class="float-btn"
                                       text="👈Like"
                                       color="#8ba38d"
                                       type="primary"
                                       @click="viewQuestions(key)"
              />
                <van-goods-action-button class="float-btn-right"
                                         text="Dislike👉"
                                         round
                                         style="border: solid #7f8182; padding: 0; color: #7f8182"
                                         @click="viewQuestions(key)"
                />
            </div>
            </b-col>
          </b-row>
        </van-tab>
      </van-tabs>
    </b-container>
  </div>
</template>

<script>
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
    };
  },
  methods: {
    viewQuestions(id) {
      this.$router.push({path: '/events/view/'+id});
    }
  }
};
</script>

<style>

.van-tabs__wrap {
  display: none !important;
}

.card-img {
  max-width: 100%;
  min-height: 100%;
  display: block;
}

.float-btn {
  width: 30%;
  font-size: 20px;
  float: left;
  margin: 5px;
}

.float-btn-right {
  width: 30%;
  font-size: 20px;
  float: right;
  margin: 5px;
}
</style>
