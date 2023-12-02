<template>
  <div class="auth-back">
    <div class="auth-card">
      <h1>Login to your account</h1>

      <form @submit.prevent="login(user)" class="form">
        <label for="value" class="form__label">Username</label>

        <InputText
          id="authpage-input-username"
          type="text"
          class="form__input"
          v-model="user.username"
        />

        <label class="form__label" for="value">Password</label>

        <Password id="value" v-model="user.password" type="text" class="form__input" toggleMask />

        <Button class="form__btn" type="submit" label="Login" />
      </form>
    </div>
  </div>
</template>

<script setup>
import InputText from 'primevue/inputtext'
import Password from 'primevue/password'
import Button from 'primevue/button'
import { auth } from '@/stores/auth'
import { ref } from 'vue'
import { botControl } from '@/stores/botControl'
import { useRouter } from 'vue-router'

const router = useRouter()

const storeBot = botControl()
const { getBots } = storeBot

getBots()
  .then(() => {
    router.push({ name: 'home' })
  })
  .catch((err) => {
    console.log('', err)
  })
const authStore = auth()

const { login } = authStore
const user = ref({
  username: '',
  password: ''
})
</script>

<style lang="scss" scoped>
.auth-back {
  display: flex;
  justify-content: center;
  align-items: flex-start;
  background: #f1f4f9;
  width: 100vw;
  height: 100vh;
}
.auth-card {
  display: flex;
  justify-content: flex-start;
  flex-direction: column;
  align-items: center;
  background: #fff;
  width: 50%;
  height: 50%;
  margin: 10% 0 0 0;
  padding: 50px 0 0 0;
  border-radius: 10px;
  color: #414040;
  box-shadow: 3px 4px 28px 17px rgba(34, 60, 80, 0.2);
  max-width: 500px;
  max-height: 600px;
  overflow: auto;
}

.form {
  display: flex;
  justify-content: flex-start;
  flex-direction: column;
  align-items: center;
  width: 100%;
  height: 100%;
  padding: 20px;
  // .form__label

  &__label {
    align-self: flex-start;
    margin: 5px 0 3px;
  }

  // .form__input

  &__input {
    width: 100%;
    height: 40px;
    margin: 0 0 20px;

    border-radius: 6px;
    // padding: 0 10px;

    &:deep(.p-icon){
      position: absolute;
      right: 10px;
      top: 50%;
      transform: translate(0, -50%);
    }
  }

  &:deep(.p-inputtext) {
    width: 100%;
    padding: 0 10px;
    border-radius: 6px;
  }

  // .form__btn

  &__btn {
    width: 100%;
    height: 40px;

    margin: 30px 0 0 0;
    background: #266ac5;
    color: #fff;
    border-radius: 6px;

    font-size: 18px;
    border: none;
  }
}
</style>
