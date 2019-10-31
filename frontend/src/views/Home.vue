<template>
  <div>
    <h1>Hello here</h1>
  </div>
</template>

<script>
export default {
  name: 'home',

  async created () {
    await this.$store.dispatch('getCurrentUser')

    if (!this.$store.state.user.current) {
      this.$router.push('login')
    }
  }
}
</script>
