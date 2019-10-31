<template>
  <b-container class="home" fluid>
    <Navbar/>
    <DatePicker/>
    <ProductivityChart/>
    <ProductivityTable/>
  </b-container>
</template>

<script>
import Navbar from '@/components/Navbar'
import DatePicker from '@/components/DatePicker'
import ProductivityTable from '@/components/ProductivityTable'
import ProductivityChart from '@/components/ProductivityChart'

export default {
  name: 'home',

  components: {
    Navbar,
    DatePicker,
    ProductivityTable,
    ProductivityChart
  },

  async created () {
    await this.$store.dispatch('getCurrentUser')

    if (!this.$store.state.user.current) {
      this.$router.push('login')
    }
  }
}
</script>

<style lang="scss">
  .home {
    padding: 0;
  }
</style>
