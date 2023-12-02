<template>
  <div class="menu">
    <h1 class="title">
      {{ title }}
    </h1>

    <PanelMenu v-model:expandedKeys="expandedKeys" :model="items" class="pannel p-panelmenu-panel">
    </PanelMenu>

    <Button label="Logout" class="button" @click="logouter" />
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import PanelMenu from 'primevue/panelmenu'
import { display } from '@/stores/display'
import Button from 'primevue/button'
import { auth } from '@/stores/auth'
import { useRouter } from 'vue-router'

const router = useRouter()

// import { storeToRefs } from 'pinia'

const authStore = auth()

const { logout } = authStore

const logouter = () => {
  logout().then(() => {
        router.push({name: "login"})
    }).catch((err) => {
        console.log(err);
    });
}

const storeD = display()
const { updateDisplay } = storeD
// const { pathArr } = storeToRefs(storeD)

const title = 'Mai Bot Manager'

const expandedKeys = ref({})

// const path = ref('')

watch(expandedKeys, (to, old) => {
  const newObj = Object.keys(to)
  const oldObj = Object.keys(old)

  let find
  if (newObj.length > oldObj.length) {
    find = newObj.filter((el) => !oldObj.includes(el))
  } else {
    find = oldObj.filter((el) => !newObj.includes(el))
  }

  if (isNaN(Number(find[0]))) updateDisplay(find[0])

  return
})

const items = ref([
  {
    key: '0',
    label: 'Bots',
    icon: '@/components/icons/icon-plus.svg',
    items: [
      {
        key: 'botList',
        label: 'List',
        icon: 'plus'
      },
      {
        key: 'botTest',
        label: 'Testing',
        icon: 'plus'
      },
      {
        key: 'statsList',
        label: 'Stats',
        icon: 'plus'
      }
    ]
  },
  {
    key: '1',
    label: 'Channels',
    icon: 'pi pi-fw pi-pencil',
    items: [
      {
        key: 'chanelList',
        label: 'List',
        icon: 'pi pi-fw pi-align-left'
      },
      {
        key: 'botPost',
        label: 'Testing',
        icon: 'pi pi-fw pi-align-right'
      },
      {
        key: 'chStatsList',
        label: 'Stats',
        icon: 'pi pi-fw pi-align-center'
      }
    ]
  },
  {
    key: 'swagger',
    label: 'Swagger API',
    icon: 'pi pi-fw pi-calendar'
  }
])
</script>

<style lang="scss" scoped>
.menu {
  display: flex;
  flex-direction: column;

  .title {
    font-size: 24px;
    padding: 0 0 50px 0;
  }

  .pannel {
    font-size: 18px;
    border-radius: 10px;
    margin-bottom: 1rem;
  }
}
.button {
  border: 3px solid #cfcfcf;
  width: 100%;
  margin: auto 0 30px;
  min-height: 40px;
  font-size: 18px;

  border-radius: 10px;
  background: #f3f3f3
}
</style>

<style>
.p-panelmenu-panel {
  /* padding: 20px 5px; */
  margin: 10px 0;
}
.p-panelmenu-header {
  padding: 20px 5px;
}

.p-menuitem-link {
  height: 100%;
}
/* .p-panelmenu, .p-menuitem-text {
    line-height: 100%;
} */
.p-menuitem-content {
  height: 20px;
}
.p-menuitem {
  padding: 0 0 20px 25px;
}
.p-icon {
  position: absolute;
  right: 10px;
}

.card {
  padding: 2rem;
  border-radius: 10px;
  margin-bottom: 1rem;
}
</style>
