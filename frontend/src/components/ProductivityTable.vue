<template>
  <b-container class="producivity">
    <b-table small head-variant="dark" bordered hover :fields="fields" :items="items"></b-table>
  </b-container>
</template>

<script>
export default {
  name: 'ProductivityTable',

  data () {
    return {
      fields: [
        {
          key: 'worker',
          label: 'Работник',
          sortable: true
        },
        {
          key: 'hour',
          label: 'Час',
          sortable: true
        },
        {
          key: 'payload',
          label: 'Урожай (кг)',
          sortable: true
        }
      ]
    }
  },

  computed: {
    items () {
      if (this.$store.state.productivity.workers) {
        return this.$store.state.productivity.workers
      } else {
        return undefined
      }
    }
  }
}
</script>

<style lang="scss">
.producivity {
  padding: 0;

  table th, td {
    outline: none;
    text-align: center;
  }
}
</style>
