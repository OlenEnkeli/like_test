import Vue from 'vue'
import Vuex from 'vuex'
import user from './user'
import productivity from './productivity'

Vue.use(Vuex)

export default new Vuex.Store({
  modules: {
    user,
    productivity
  },
  state: {
  },
  mutations: {
  },
  actions: {
  }
})
