<template>
  <p>Signing in...</p>
</template>

<script>

import { setToken, validateSecret } from '~/utils/auth';

export default {
  async mounted() {
    const { token, secret } = this.$route.query;

    if (!validateSecret(secret) || !token) {
      console.error('Something happened with the Sign In request');
    }

    setToken(token);
    this.$store.commit('setToken', token);
    await this.$store.dispatch('fetchUserInfo');

    this.$router.replace('/');
  },
};
</script>
