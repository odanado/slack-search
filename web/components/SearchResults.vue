<template>
  <div>
    <el-table
      :data="convertedResults"
      style="width: 100%">
      <el-table-column
        prop="formatedDate"
        label="Date"
        width="170"/>
      <el-table-column
        prop="channelName"
        label="Channel"
        width="80"/>
      <el-table-column
        prop="userName"
        label="User"
        width="100"/>
      <el-table-column
        prop="text"
        label="Text"/>
      <el-table-column
        label="Link"
        width="90">
        <template slot-scope="scope">
          <div class="link">
            <a
              v-if="scope.row.link"
              target="_blank"
              :href="scope.row.link">Link</a>
            <el-button
              v-else
              @click="fetchLink(scope.row)"
              type="text"
              size="medium">
              Fetch Link
            </el-button>
          </div>
        </template>
      </el-table-column>
    </el-table>
    <div v-if="total">
      <el-pagination
        @current-change="currentChange"
        background
        layout="prev, pager, next"
        :total="total"/>
    </div>
  </div>
</template>

<script>

import Vue from 'vue';
import dateFormat from 'dateformat';
import Slack from 'slack';

export default {
  props: {
    results: {
      type: Array,
      default() {
        return [];
      },
    },
    total: {
      type: Number,
      default() {
        return null;
      },
    },
    id2user: {
      type: Map,
      default() {
        return new Map();
      },
    },
    id2channel: {
      type: Map,
      default() {
        return new Map();
      },
    },
  },
  computed: {
    convertedResults() {
      this.results.forEach((x) => {
        this.id2user.forEach((v, k) => {
          const pattern = `<@${k}>`;
          const replacement = `@${v}`;
          x.text = x.text.replace(pattern, replacement);
        });
        x.channelName = this.id2channel.get(x.channel);
        x.userName = this.id2user.get(x.user);
        x.formatedDate = dateFormat(new Date(x.timestamp * 1000), 'yyyy-mm-dd HH:MM:ss');
      });

      return this.results;
    },
  },
  methods: {
    async fetchLink(row) {
      const token = this.$store.getters.getSlackToken;
      const { timestamp, channel } = row;
      const res = await Slack.chat.getPermalink({ token, message_ts: timestamp, channel });
      if (res.ok) {
        Vue.set(row, 'link', res.permalink);
      }
    },
    currentChange(newPage) {
      this.$store.commit('setCurrentPage', newPage - 1);
      this.$store.dispatch('searchText');
    },
  },
};
</script>

<style scoped>
.link {
  text-align: center;
}
.el-pagination {
  margin-top: 20px;
  text-align: center;
}
</style>
