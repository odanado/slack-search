<template>
  <el-container>
    <el-header>
      <Header :imageUrl="$store.state.imageUrl"/>
    </el-header>
    <el-main>
      <nuxt/>
    </el-main>
  </el-container>
</template>


<script>
import Header from '~/components/Header.vue';

export default {
  components: {
    Header,
  },
};

</script>

<style>
.el-header {
  background-color: #409EFF;
  /* padding: 10px 10px; */
}
html {
  font-family: "Source Sans Pro",
  -apple-system, BlinkMacSystemFont, "Segoe UI",
  Roboto, "Helvetica Neue", Arial, sans-serif;
  font-size: 16px;
  word-spacing: 1px;
  -ms-text-size-adjust: 100%;
  -webkit-text-size-adjust: 100%;
  -moz-osx-font-smoothing: grayscale;
  -webkit-font-smoothing: antialiased;
  box-sizing: border-box;
}
</style>
