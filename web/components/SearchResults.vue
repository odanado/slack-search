<template>
  <el-table
    :data="tableData"
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
    tableData: {
      type: Array,
      default() {
        return [];
      },
    },
  },
};
</script>
