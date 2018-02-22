export default async function ({ store, redirect, route }) {
  if (route.path === '/auth/signed-in') {
    return undefined;
  }
  await store.dispatch('validateToken');
  if (!store.getters.isAuthenticated) {
    return redirect('/auth/sign-in');
  }

  return undefined;
}
