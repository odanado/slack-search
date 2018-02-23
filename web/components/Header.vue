<template>
  <el-row>
    <el-col :span="4">
      <div class="text">Slack Search</div>
    </el-col>
    <el-col :span="17">
      <SearchBox
        v-if="$store.getters.isAuthenticated"
        class="search-box" />
    </el-col>
    <el-col
      :span="2"
      :offset="1">
      <img
        v-if="$store.getters.isAuthenticated"
        :src="imageUrl">
    </el-col>
  </el-row>
</template>


<script>
import SearchBox from '~/components/SearchBox.vue';

export default {
  components: {
    SearchBox,
  },
  props: {
    imageUrl: {
      type: String,
      default: null,
    },
  },
};

</script>

<style scoped>

.text {
  color: white;
  line-height: 60px;
  font-size: 18px;
  text-align: center;
}

.search-box {
  margin-top: 10px;
}

img {
  width: 50px;
  height: 50px;
  border-radius: 100px;
  margin: auto 0;
  margin-top: 5px;
}
</style>

