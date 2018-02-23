<template>
  <el-table
    :data="convertedResults"
    style="width: 100%">
    <el-table-column
      prop="timestamp"
      label="Date"
      width="180"/>
    <el-table-column
      prop="channel"
      label="Channel"
      width="180"/>
    <el-table-column
      prop="text"
      label="Text"/>
  </el-table>
</template>

<script>
export default {
  props: {
    results: {
      type: Array,
      default() {
        return [];
      },
    },
    id2user: {
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
      });

      return this.results;
    },
  },
};
</script>
