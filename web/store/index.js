/* eslint no-shadow: ["error", { "allow": ["state"] }] */

import Vue from 'vue';
import Vuex from 'vuex';
import Slack from 'slack';
import axios from 'axios';
import jwtDecode from 'jwt-decode';

import { getTokenFromCookie } from '~/utils/auth';

Vue.use(Vuex);

export const state = {
  token: null,
  name: null,
  imageUrl: null,
  searchResults: [],
};

export const mutations = {
  setToken(state, token) {
    state.token = token || null;
  },
  setName(state, name) {
    state.name = name || null;
  },
  setImageUrl(state, imageUrl) {
    state.imageUrl = imageUrl || null;
  },
  setSearchResults(state, searchResults) {
    state.searchResults = searchResults || null;
  },
};

export const actions = {
  async fetchUserInfo({ commit, getters }) {
    const { slack } = getters.decodeToken;
    const token = slack.access_token;
    const user = slack.user_id;

    if (token && user) {
      const data = await Slack.users.info({ token, user });
      commit('setName', data.user.name);
      commit('setImageUrl', data.user.profile.image_192);
    }
  },
  async validateToken({ state, commit }) {
    if (!state.token) return;
    const url = `${process.env.SERVER_URL}/validate_token`;
    const response = await axios.get(url, {
      params: { token: state.token },
    });

    const { status } = response.data;
    if (status !== 'ok') {
      commit('setToken', null);
    }
  },
  async searchText({ commit, state }, text) {
    if (!text) return;
    const url = `${process.env.SERVER_URL}/search`;

    const response = await axios.get(url, {
      params: { token: state.token, text },
    });

    const { status, results } = response.data;
    if (status === 'ok') {
      commit('setSearchResults', results);
    } else {
      commit('setToken', null);
    }
  },
  async nuxtServerInit({ commit, dispatch }, { req }) {
    const token = getTokenFromCookie(req);
    if (token) {
      commit('setToken', token);
      await dispatch('fetchUserInfo');
    }
  },
};

export const getters = {
  isAuthenticated(state) {
    return !!state.token;
  },
  decodeToken(state) {
    return jwtDecode(state.token);
  },
};

const createStore = () => new Vuex.Store({
  state,
  getters,
  actions,
  mutations,
});

export default createStore;
