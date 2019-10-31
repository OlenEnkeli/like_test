<template>
  <b-container class="login">
    <b-jumbotron>
        <template v-slot:header>LikeTest auth</template>
        <template v-slot:lead>
            Для доступа к приложению, пожалуйста, авторизуйтесь
        </template>
        <hr class="my-4">
        <LoginForm/>
    </b-jumbotron>

  </b-container>
</template>

<script>
import LoginForm from '@/components/LoginForm'

export default {
  name: 'Login',
  components: {
    LoginForm
  }
}
</script>

<style lang="scss" scoped>
.login {
    margin-top: 5%;
}
</style>
