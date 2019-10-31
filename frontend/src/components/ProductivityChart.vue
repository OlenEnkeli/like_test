<template>
  <b-container>
    <ve-line :data="items"></ve-line>
  </b-container>
</template>

<script>
export default {
  name: 'ProductivityChart',

  computed: {
    items () {
      if (this.$store.state.productivity.workers_chart) {
        return this.$store.state.productivity.workers_chart
      } else {
        return undefined
      }
    }
  }
}
</script>
