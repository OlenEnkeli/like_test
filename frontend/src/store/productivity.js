import moment from 'moment'

import productivityAPI from '@/api/productivity'

export default {

  state: {
    workers: [],
    workers_chart: {},
    workdates: undefined
  },

  mutations: {
    setWorkers (state, workers) {
      let result = []
      let productivities = {}

      state.workers_chart = {
        columns: ['time'],
        rows: []
      }

      workers.forEach(worker => {
        let name = `${worker.worker.name} ${worker.worker.surname}`

        state.workers_chart.columns.push(name)

        for (let key in worker.productivity) {
          if (!(key in productivities)) {
            productivities[key] = {}
          }

          productivities[key][name] = worker.productivity[key]

          result.push({
            worker: name,
            hour: parseInt(key),
            payload: worker.productivity[key] / 1000
          })
        }
      })

      for (let key in productivities) {
        state.workers_chart.rows.push({
          time: key,
          ...productivities[key]
        })
      }

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
