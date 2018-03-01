/* eslint no-shadow: ["error", { "allow": ["state", "getters"] }] */

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
  searchResults: {},
  targetText: null,
  currentPage: 0,
  usersList: [],
  channelsList: [],
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
    state.searchResults = searchResults || {};
  },
  setTargetText(state, targetText) {
    state.targetText = targetText || null;
  },
  setCurrentPage(state, currentPage) {
    state.currentPage = currentPage || 0;
  },
  setUsersList(state, usersList) {
    state.usersList = usersList || [];
  },
  setChannelsList(state, channelsList) {
    state.channelsList = channelsList || [];
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
  async fetchUsersList({ commit, getters }) {
    const { slack } = getters.decodeToken;
    const token = slack.access_token;

    if (token) {
      const data = await Slack.users.list({ token });
      commit('setUsersList', data.members);
    }
  },
  async fetchChannelsList({ commit, getters }) {
    const { slack } = getters.decodeToken;
    const token = slack.access_token;

    if (token) {
      const data = await Slack.channels.list({ token });
      commit('setChannelsList', data.channels);
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
  async searchText({ commit, state }) {
    const { targetText, currentPage } = state;
    if (!targetText) return;
    const url = `${process.env.SERVER_URL}/search`;

    const response = await axios.get(url, {
      params: { token: state.token, text: targetText, from: currentPage * 10 },
    });

    const { status, hits, total } = response.data;
    if (status === 'ok') {
      commit('setSearchResults', { hits, total });
    } else {
      commit('setToken', null);
    }
  },
  async nuxtServerInit({ commit, dispatch }, { req }) {
    const token = getTokenFromCookie(req);
    if (token) {
      commit('setToken', token);
      await Promise.all([
        dispatch('fetchUserInfo'),
        dispatch('fetchUsersList'),
        dispatch('fetchChannelsList'),
      ]);
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
  getSlackToken(state, getters) {
    const { slack } = getters.decodeToken;
    return slack.access_token;
  },
  id2user(state) {
    const users = new Map(state.usersList.map(x => [x.id, x.name]));
    const bots = new Map(state.usersList.filter(x => x.is_bot)
      .map(x => [x.profile.bot_id, x.name]));
    return new Map([...users, ...bots]);
  },
  userAvatars(state) {
    const users = new Map(state.usersList.map(x => [x.id, x.profile.image_32]));
    const bots = new Map(state.usersList.filter(x => x.is_bot)
      .map(x => [x.profile.bot_id, x.profile.image_32]));
    return new Map([...users, ...bots]);
  },
  id2channel(state) {
    return new Map(state.channelsList.map(x => [x.id, x.name]));
  },
};

const createStore = () => new Vuex.Store({
  state,
  getters,
  actions,
  mutations,
});

export default createStore;
