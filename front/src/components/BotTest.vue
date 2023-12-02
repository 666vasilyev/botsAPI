<template>
  <Card>
    <template #content>
      <div class="p-card-body">
        <Dropdown
          v-model="currBot"
          @update:modelValue="updateCurrBot"
          :options="botList"
          :style="{ color: Object.keys(currBot).length === 0 ? '#5c5959' : '#000' }"
          optionLabel="name"
          placeholder="select bot"
          class="drop-list"
        />

        <Dropdown
          v-if="Object.keys(currBot).length !== 0"
          v-model="currChannel"
          :options="filtredChannels"
          :style="{ color: Object.keys(currChannel).length === 0 ? '#5c5959' : '#000' }"
          optionLabel="channel"
          placeholder="select channel"
          class="drop-list"
        />

        <Button label="Test" class="button" @click="test" />

        <InputText type="text" v-model="result" disabled class="label" />
        <Textarea
          ref="area"
          rows="16"
          v-model="textArea"
          class="text-area"
          disabled
          :autoResize="true"
          @load="scroll"
        />
      </div>
    </template>
  </Card>
</template>

<script setup>
import Card from 'primevue/card'
import Dropdown from 'primevue/dropdown'
import InputText from 'primevue/inputtext'
import Button from 'primevue/button'
import Textarea from 'primevue/textarea'
import { ref } from 'vue'
import { botControl } from '@/stores/botControl'
import { storeToRefs } from 'pinia'
// import { auth } from '@/stores/auth'

// const authStore = auth()

// const { logout } = authStore
// logout()

const storeBot = botControl()
const { botList, channels } = storeToRefs(storeBot)
const { getBots, getChanels, statCheck } = storeBot

getBots()
getChanels()

const textArea = ref('')

const result = ref('Result')

const currBot = ref({})
const updateCurrBot = (event) => {
  filterChannelsByName(event)
}

const currChannel = ref({})
const filtredChannels = ref([])

const filterChannelsByName = (item) => {
  filtredChannels.value = channels.value.filter((el) => el.bot_id === item.id)
}

const area = ref(null)
const test = () => {
  statCheck({ botId: currBot.value.id, channelId: currChannel.value.channel })
    .then((res) => {
      const text = Object.entries(res).reduce(
        (prev, [key, val]) => (prev += key + ': ' + val + '\n'),
        ''
      )
      textArea.value += '\n' + text + '\n'
      scrollArea()
    })
    .catch((err) => {
      scrollArea()
      if (err?.response?.status === 409) {
        textArea.value += err.response.data.detail + '\n'
        return
      }
      textArea.value += 'Request ERROR' + '\n'
    })
}

const scrollArea = () => {
  area.value.$el.scrollTo(0, area.value.$el.scrollHeight)
}
</script>

<style lang="scss" scoped>
.drop-list {
  border: 3px solid #1c273d;
  width: 100%;
  color: #000;

  margin: 20px 0;

  padding: 10px;
  &::placeholder {
    color: #5c5959;
  }
}
.input {
  margin: 20px 0 20px 0;
  border: 3px solid #1c273d;
  width: 100%;
  color: #000;

  padding: 10px;
}

.button {
  border: 3px solid #1c273d;
  width: 50%;
  margin: 0 0 40px auto;
  min-height: 35px;
  font-size: 18px;
}

.text-area {
  border: 3px solid #1c273d;
  width: 100%;
  height: 40%;
  min-height: 300px;

  padding: 20px;
  overflow: auto;
  box-sizing: border-box;
  max-height: 300px;

  overflow: auto !important;
}

.label {
  position: relative;
  transform: translate(10px, 10px);
  margin: 0 auto 0 0;
  border: none;
  text-align: center;
  width: 20%;
  background: #fff;
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
