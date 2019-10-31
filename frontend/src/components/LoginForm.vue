<template>
  <div class="login_form">

    <b-alert class="login_form__alert" :show="login_failed" variant="danger" dismissible @dismissed="login_failed=false">
      <p>Не удалось войти. Проверьте введенные данные</p>
    </b-alert>

    <b-form @submit="login">
      <b-form-group>
        <b-form-input id="login" v-model="form.login" type="text" required placeholder="Логин"></b-form-input>
      </b-form-group>

      <b-form-group>
        <b-form-input id="password" v-model="form.password" type="password" required placeholder="Пароль"></b-form-input>
      </b-form-group>

      <b-button block type="submit" variant="outline-info">Войти как менеджер</b-button>
    </b-form>
  </div>
</template>

<script>

export default {
  name: 'LoginForm',

  data () {
    return {
      login_failed: false,
      form: {
        login: '',
        password: ''
      }
    }
  },

  async created () {
    await this.$store.dispatch('getCurrentUser')

    if (this.$store.state.user.current) {
      this.$router.push({ name: 'home' })
    }
  },

  methods: {
    async login (evt) {
      evt.preventDefault()

      await this.$store.dispatch('login', this.form)
      await this.$store.dispatch('getCurrentUser')

      if (this.$store.state.user.current) {
        this.$router.push({ name: 'home' })
      } else {
        this.login_failed = true
      }
    }
  }
}

</script>

<style lang="scss" scoped>
.login_form {
  &__alert {
    p {
      margin: 0;
    }
  }
}
</style>
