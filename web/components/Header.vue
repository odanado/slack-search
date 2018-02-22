<template>
  <el-row>
    <el-col :span="20">
      <SearchBox />
    </el-col>
    <el-col
      :span="2"
      :offset="2">
      <img :src="imageUrl">
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

img {
  width: 50px;
  height: 50px;
  border-radius: 100px;
  margin: auto 0;
}
</style>

