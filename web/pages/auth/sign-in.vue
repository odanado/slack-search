<template>
  <div class="container">
    <a :href="url">
      <img src="~/assets/slack-logo.png">
    </a>
  </div>
</template>

<script>
import { getOAuthSlackUrl } from '~/utils/slack';

export default {
  data() {
    return {
      url: '',
    };
  },
  mounted() {
    const url = getOAuthSlackUrl();
    this.url = url;
  },
};
</script>
