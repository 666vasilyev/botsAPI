import './assets/main.css'
// import axios from 'axios';

import { createApp } from 'vue';
import { createPinia } from 'pinia';
import PrimeVue from 'primevue/config';

import App from './App.vue';
import router from './router';

// axios.defaults.baseURL = import.meta.env.VITE_SERVE;
const app = createApp(App);

app.use(createPinia());
app.use(router);
app.use(PrimeVue);
app.mount('#app');
