import moment from 'moment'

import productivityAPI from '@/api/productivity'

export default {

  state: {
    workers: [],
    workdates: undefined
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
    },

    setWorkdates (state, workdates) {
      state.workdates = {
        to: moment(workdates.min_date).toDate(),
        from: moment(workdates.max_date).toDate()
      }
    }
  },

  actions: {
    async getProductivity ({ commit }, date) {
      const workers = await productivityAPI.productivity(date)
      if (workers !== 404) {
        commit('setWorkers', workers)
      }
    },

    async getWorkdates ({ commit }) {
      const workdates = await productivityAPI.workdates()
      if (workdates !== 404) {
        commit('setWorkdates', workdates)
      }
    }
  }
}
