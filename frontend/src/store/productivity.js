import productivityAPI from '@/api/productivity'

export default {

  state: {
    workers: []
  },

  mutations: {
    setWorkers (state, workers) {
      let result = []

      workers.forEach(worker => {
        for (let key in worker.productivity) {
          result.push({
            worker: `${worker.worker.name} ${worker.worker.surname}`,
            hour: key,
            payload: worker.productivity[key] / 1000
          })
        }
      })

      state.workers = result
    }
  },

  actions: {
    async getProductivity ({ commit }, date) {
      const workers = await productivityAPI.productivity(date)
      if (workers !== 404) {
        commit('setWorkers', workers)
      }
    }
  }
}
