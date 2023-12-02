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

        <InputText type="text" v-model="msg" class="label" disabled/>
        <Textarea rows="16" v-model="message" class="text-area" :autoResize="true" />

        <Button label="Post" class="button" @click="test" />

        <InputText type="text" v-model="result" class="label" disabled/>
        <Textarea
          ref="area"
          rows="16"
          v-model="textArea"
          class="text-area"
          disabled
          :autoResize="true"
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

const storeBot = botControl()
const { botList, channels } = storeToRefs(storeBot)
const { getBots, postMessageTg } = storeBot

getBots()
//getChanels()

const textArea = ref('')

const result = ref('Result')
const msg = ref('Message')

const message = ref('')

const currBot = ref({})
const updateCurrBot = (event) => {
  currChannel.value = {}

  filterChannelsByName(event)
}

const filterChannelsByName = (item) => {
  filtredChannels.value = channels.value.filter((el) => el.bot_id === item.id)
}

const currChannel = ref({})
const filtredChannels = ref([])

const test = () => {
  postMessageTg({
    botId: currBot.value.id,
    channelId: currChannel.value.channel,
    message: message.value
  })
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
    .finally(() => (message.value = ''))
}

const area = ref(null)
const scrollArea = () => {
  area.value.$el.scrollTo(0, area.value.$el.scrollHeight)
}
</script>

<style lang="scss" scoped>
.drop-list {
  border: 3px solid #1c273d;
  width: 100%;
  color: #000;

  padding: 10px;
  margin: 20px 0;
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
  margin: 30px 0 30px auto;
  min-height: 35px;
  font-size: 18px;
}

.text-area {
  border: 3px solid #1c273d;
  width: 100%;
  min-height: 250px;
  padding: 15px;
  max-height: 250px;

  overflow: auto !important;
  background: #fff;
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
:deep(.p-card-content) {
  border: 3px solid #1c273d;
  padding: 2% 5% 0 ;
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100%;
  overflow: auto;
}
</style>

<style>
.p-card-body {
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100%;
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
