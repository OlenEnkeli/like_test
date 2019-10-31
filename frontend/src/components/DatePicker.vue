<template>
  <b-container class="date">
    <Datepicker class="date__picker" v-model="pickedDate" @input="pickDate" :language="ru" placeholder="Выберите дату"/>
  </b-container>
</template>

<script>
import Datepicker from 'vuejs-datepicker'
import { en, ru } from 'vuejs-datepicker/dist/locale'

export default {
  name: 'DatePicker',

  components: {
    Datepicker
  },

  data () {
    return {
      pickedDate: new Date(2018, 0, 2),

      en: en,
      ru: ru
    }
  },

  methods: {
    async pickDate () {
      let formatDate = this.pickedDate.toISOString().substring(0, 10)
      await this.$store.dispatch('getProductivity', formatDate)
    }
  },

  async created () {
    this.pickDate()
  }
}
</script>

<style lang="scss">
.date {
  padding: 1.5em 0;

  &__picker {
    width: 300px;
    margin: 0 auto;

    input {
      width: 300px;
      outline: none;
      padding: 0.5em 0.8em;
      text-align: center;
      color: #1a6d81;
    }
  }
}
</style>
