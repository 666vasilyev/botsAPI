<template>
  <div class="modal-back">
    <div class="modal-add" @click.capture="isValid = true">
      <Button label="X" class="button-close" @click="$emit('close')" />

      <label for="modal-add-name" :style="{ color: chekOnError(params.name) ? 'red' : '' }"
        ><span v-if="chekOnError(params.name)">Empty:</span> Name</label
      >
      <InputText
        id="modal-add-name"
        type="text"
        v-model="params.name"
        class="input"
        :class="{ 'p-invalid': chekOnError(params.name) }"
      />

      <label for="modal-add-alias" :style="{ color: chekOnError(params.alias) ? 'red' : '' }"
        ><span v-if="chekOnError(params.alias)">Empty:</span> Alias</label
      >
      <InputText
        id="modal-add-alias"
        type="text"
        v-model="params.alias"
        class="input"
        :class="{ 'p-invalid': chekOnError(params.alias) }"
      />

      <label
        for="modal-add-textdesc"
        :style="{ color: chekOnError(params.description) ? 'red' : '' }"
        ><span v-if="chekOnError(params.description)">Empty:</span> Desctiption</label
      >
      <Textarea
        id="modal-add-textdesc"
        rows="16"
        v-model="params.description"
        class="text-area"
        :class="{ 'p-invalid': chekOnError(params.description) }"
        :autoResize="true"
      />

      <label for="modal-add-tokentg" :style="{ color: chekOnError(params.botToken) ? 'red' : '' }"
        ><span v-if="chekOnError(params.botToken)">Empty:</span> Bot Token</label
      >
      <InputText
        id="modal-add-tokentg"
        type="text"
        v-model="params.botToken"
        class="input"
        :class="{ 'p-invalid': chekOnError(params.botToken) }"
      />

      <Button label="Add" class="button" @click="createReqBot(params)" />
    </div>
  </div>
</template>

<script setup>
import InputText from 'primevue/inputtext'
import Button from 'primevue/button'
import Textarea from 'primevue/textarea'
import { botControl } from '@/stores/botControl'
import { ref } from 'vue'

const emit = defineEmits(['close','updateTable'])

const isValid = ref(true)

const storeBot = botControl()
const { createBot } = storeBot

const params = ref({
  alias: '',
  description: '',
  name: '',
  botToken: ''
})

const createReqBot = () => {
  isValid.value = !Object.values(params.value).includes('')
  if (isValid.value) {
    try {
      createBot(params.value).then(() => {
        emit('updateTable')
      }).catch(() => {
        alert('Request error try again later')
      });
    } catch {
      alert('Create error, check params or try again later')
    }
  }
}

const chekOnError = (value) => {
  return !!(value === '' && !isValid.value)
}
// {
//   "alias": "from_botsapi_bot",
//   "description": "string",
//   "name": "administration_from_botsapi_bot",
//   "bot_token": "6070753137:AAGvJjohwwaSQk7u4n1NWsxbyg9Uq3mLoX0"
// }
</script>

<style lang="scss" scoped>
.modal-back {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 100%;

  background: #00000075;
}
.button-close {
  border-radius: 45%;
  font-weight: 900;
  border: 1px solid #1c273d;

  margin: 0 0 10px 0;
}

.modal-add {
  display: flex;
  // overflow: auto;
  justify-content: center;
  align-items: flex-end;
  flex-direction: column;

  padding: 20px;
  width: 50%;
  // height: 50%;
  max-width: 800px;
  max-height: 1000px;

  background: #fff;
  color: #1c273d;

  box-shadow: 8px 7px 38px 30px rgba(206, 213, 217, 0.2);
}

.drop-list {
  border: 3px solid #1c273d;
  width: 100%;
  color: #000;

  padding: 10px;
  &::placeholder {
    color: #5c5959;
  }
}
.input {
  margin: 0 0 20px 0;
  border: 3px solid #1c273d;
  width: 100%;
  color: #000;

  padding: 10px;
}

.button {
  border: 3px solid #1c273d;
  width: 50%;
  margin: 30px 0 30px auto;
  min-height: 30px;
}

.text-area {
  border: 3px solid #1c273d;
  width: 100%;
  min-height: 150px;
  margin: 0 0 20px 0;
}

.label {
  position: relative;
  transform: translate(10px, 10px);
  margin: 0 auto 0 0;
  border: none;
  text-align: center;
  width: 20%;
}

.p-invalid {
  border: 3px solid red;
}
</style>

<style>
.p-card-body {
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100%;
}
.p-card-content {
  border: 3px solid #1c273d;
  padding: 10%;
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100%;
  overflow: auto;
}

.p-dropdown::placeholder {
  color: #5c5959;
}
.p-dropdown-panel {
  color: #000;
  background: #fff;
  border: 3px solid #1c273d;
  padding: 10px;
}
</style>
