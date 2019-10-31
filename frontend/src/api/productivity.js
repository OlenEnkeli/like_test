import axios from './index'

export default {
  async productivity (date) {
    try {
      const workers = await axios.get(`/productivity?date=${date}`)
      return workers.data
    } catch (error) {
      return error.response.status
    }
  }
}
