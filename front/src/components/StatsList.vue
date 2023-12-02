<template>
  <Card>
    <!-- <template #header>
      <Button label="Add Bot" class="button" @click="isAddBot = true" />
    </template> -->
    <template #content>
      <div class="p-card-body">
        <DataTable :value="botList" tableStyle="min-width: 20px" class="table">
          <Column field="id" header="Id" sortable style="width: 10%"></Column>
          <Column field="alias" header="Name" sortable style="width: 25%"></Column>
          <Column field="active" header="Active" sortable style="width: 15%">
            <template #body="slotProps">
              <Checkbox v-model="slotProps.data.active" :binary="slotProps.data.active"  disabled/>
            </template>
          </Column>
        </DataTable>
      </div>

      <teleport to="body">
        <modal-add
          v-if="isAddBot"
          class="modal"
          @close="isAddBot = false"
          @updateTable="getBots(), (isAddBot = false)"
        ></modal-add>
      </teleport>
    </template>
  </Card>
</template>

<script setup>
import Checkbox from 'primevue/checkbox'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
// import ColumnGroup from 'primevue/columngroup' // optional
// import Row from 'primevue/row'

import Card from 'primevue/card'
import { ModalAdd } from '@/components'
import { onMounted, ref } from 'vue'
import { botControl } from '@/stores/botControl'
import { storeToRefs } from 'pinia'

const storeBot = botControl()
const { getBots } = storeBot
const { botList } = storeToRefs(storeBot)
const isAddBot = ref(false)

onMounted(async () => {
  await getBots()
})
</script>

<style lang="scss" scoped>
:deep(.p-checkbox) {
  width: 20px;
  height: 20px;
  margin: 0 0 2px 5px;
  //background: #5c5959;
  border: 1px solid #000;
}

:deep(.p-card-content) {
  padding: 10% 0 0;
  padding-top: calc(10% + 30px);
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100%;
  overflow: auto;
  border: none;
}
:deep(.p-card-body) {
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100%;
  overflow: auto;
}
.table {
  color: #000;
  border: 1px solid #000;

  &:deep(td) {
    border: 1px solid #000;
    border-collapse: collapse;
  }
  &:deep(tr) {
    background: #ebe7e7;
    &:nth-of-type(2n) {
      background: #ffffff;
    }
  }
  &:deep(thead) {
    position: sticky;
    top: 0;
  }
  &:deep(th) {
    position: sticky;
    top: 0;
    border: 1px solid #000;
    border-collapse: collapse;
    position: relative;
    background: #bdb8b8;
  }

  &:deep(.p-icon) {
    position: absolute;
    right: 10px;
    top: 7px;
  }
  &:deep(.p-checkbox-icon) {
    position: relative;
    right: 0;
    left: 2px;
    top: 0;
  }
  &:deep(.p-datatable-table) {
    position: absolute;
  }
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
  margin: 20px 0 20px 0;
  border: 3px solid #1c273d;
  width: 100%;
  color: #000;

  padding: 10px;
}

.button {
  border: 3px solid #1c273d;
  width: 30%;
  margin: 0 0 0 70%;
  min-height: 30px;
}

.text-area {
  border: 3px solid #1c273d;
  width: 100%;
  height: 40%;
  min-height: 150px;
}

.label {
  position: relative;
  transform: translate(10px, 10px);
  margin: 0 auto 0 0;
  border: none;
  text-align: center;
  width: 20%;
}

.modal {
  position: absolute;
  top: 0;
}
</style>

<style>
.p-dropdown-panel {
  color: #000;
  background: #fff;
  /* border: 3px solid #1c273d; */
  padding: 10px;
}
</style>
