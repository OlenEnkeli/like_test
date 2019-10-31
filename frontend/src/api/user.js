import axios from './index'

export default {
  async login (credentials) {
    try {
      await axios.post('/login/manager', {
        login: credentials.login,
        password: credentials.password
      })
    } catch (error) {
      return error.response.status
    }
  },

  async getCurrentUser () {
    try {
      const user = await axios.get('/users/current')
      return user.data
    } catch (error) {
      return error.response.status
    }
  },

  async logout () {
    try {
      await axios.get('/logout')
    } catch (error) {
      return error.response.status
    }
  }
}
