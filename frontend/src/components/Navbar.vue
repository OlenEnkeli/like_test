<template>
  <b-navbar type="dark" variant="dark">
    <b-navbar-brand href="#" >LikeTest</b-navbar-brand>

    <b-navbar-nav>
      <b-nav-item href="#">Сбор продукции</b-nav-item>
      <b-nav-item href="#" disabled>Работники</b-nav-item>
      <b-nav-item href="#" disabled>Контроль качества</b-nav-item>
    </b-navbar-nav>

    <b-navbar-nav class="ml-auto">
      <b-nav-item-dropdown right>
          <template v-slot:button-content>
            <em>{{username}}</em>
          </template>
          <b-dropdown-item disabled class='manager-label' href="#">Менеджер</b-dropdown-item>
          <b-dropdown-item disabled href="#">Профиль</b-dropdown-item>
          <b-dropdown-item href="#">Выйти</b-dropdown-item>
      </b-nav-item-dropdown>
    </b-navbar-nav>

  </b-navbar>
</template>

<script>
export default {
  name: 'Navbar',

  computed: {
    username () {
      if (this.$store.state.user.current) {
        return `${this.$store.state.user.current.name} ${this.$store.state.user.current.surname}`
      } else {
        return ''
      }
    }
  }
}
</script>

<style lang="scss">
.manager-label{
  a.dropdown-item.disabled {
    color: #04c74e;
  }
}
</style>
