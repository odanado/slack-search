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
      <el-dropdown
        v-if="$store.getters.isAuthenticated"
        @command="handleCommand">
        <img :src="imageUrl">
        <el-dropdown-menu slot="dropdown">
          <el-dropdown-item
            disabled
            class="user-name">
            {{ userName }}
          </el-dropdown-item>
          <el-dropdown-item
            divided
            command="logout">
            Logout
          </el-dropdown-item>
        </el-dropdown-menu>
      </el-dropdown>
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
    userName: {
      type: String,
      default: null,
    },
  },
  methods: {
    async handleCommand(command) {
      if (command === 'logout') {
        await this.$store.dispatch('logout');
        this.$router.go({ path: '/', force: true });
      }
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
.user-name {
  color: #606266
}
</style>

