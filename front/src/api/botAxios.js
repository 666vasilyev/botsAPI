import axios from 'axios';
// import checkAuth from '@/components/helpers/checkAuth';
import router from '../router';
const botAxios = axios.create({
  baseURL: import.meta.env.VITE_SERVE,
  withCredentials: true
});

botAxios.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.message.includes(401)) {
      router.push({ name: 'login' })
      return;
    }

    Promise.reject(error);
  },
);

export default botAxios;
