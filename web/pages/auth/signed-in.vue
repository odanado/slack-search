<template>
  <p>Signing in...</p>
</template>

<script>

import { setToken, validateSecret } from '~/utils/auth';

export default {
  async mounted() {
    const { token, secret } = this.$route.query;

    if (!validateSecret(secret) || !token) {
      // eslint-disable-next-line
      console.error('Something happened with the Sign In request');
    }

    setToken(token);
    this.$store.commit('setToken', token);

    await Promise.all([
      this.$store.dispatch('fetchUserInfo'),
      this.$store.dispatch('fetchUsersList'),
      this.$store.dispatch('fetchChannelsList'),
    ]);

    this.$router.replace('/');
  },
};
</script>
