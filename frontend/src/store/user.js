import userAPI from '@/api/user'

export default {

  state: {
    current: undefined
  },

  mutations: {
    setUser (state, user) {
      state.current = user
    }
  },

  actions: {
    async login ({ commit }, credentials) {
      await userAPI.login(credentials)
    },

    async logout ({ commit }) {
      await userAPI.logout()
      commit('setUser', undefined)
    },

    async getCurrentUser ({ commit }) {
      const user = await userAPI.getCurrentUser()
      if (user !== 401 && 502) {
        commit('setUser', user)
      }
    }
  }
}
