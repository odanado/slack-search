<template>
  <div>
    <el-input
      v-model="text"
      placeholder="search"
      @keyup.enter.native="search(text)"/>
  </div>
</template>

<script>
export default {
  data() {
    return {
      text: null,
    };
  },
  methods: {
    search(text) {
      this.$store.commit('setTargetText', text);
      this.$store.dispatch('searchText');
    },
  },
};
</script>


<style scoped>
.el-input {
  font-size: 16px;
}

</style>
