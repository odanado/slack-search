<template>
  <div>
    <SearchResults
      :results="searchResults"
      :total="searchReusltTotal"
      :id2user="id2user"
      :id2channel="id2channel"
    />
  </div>
</template>

<script>
import { mapState, mapGetters } from 'vuex';

import SearchResults from '~/components/SearchResults.vue';

export default {
  components: {
    SearchResults,
  },
  computed: {
    ...mapState({
      searchResults: state => state.searchResults.hits,
      searchReusltTotal: state => state.searchResults.total,
    }),
    ...mapGetters([
      'id2user',
      'id2channel',
    ]),
  },
};

</script>

<style>

.title {
  font-family: "Quicksand", "Source Sans Pro",
  -apple-system, BlinkMacSystemFont, "Segoe UI",
  Roboto, "Helvetica Neue", Arial, sans-serif; /* 1 */
  display: block;
  font-weight: 300;
  font-size: 100px;
  color: #35495e;
  letter-spacing: 1px;
}

.subtitle {
  font-weight: 300;
  font-size: 42px;
  color: #526488;
  word-spacing: 5px;
  padding-bottom: 15px;
}

.links {
  padding-top: 15px;
}
</style>
