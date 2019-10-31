import axios from './index'

export default {
  async productivity (date) {
    try {
      const workers = await axios.get(`/productivity?date=${date}`)
      return workers.data
    } catch (error) {
      return error.response.status
    }
  },

  async workdates () {
    try {
      const workdates = await axios.get('/workdate')
      return workdates.data
    } catch (error) {
      return error.response.status
    }
  }
}
