import axios from 'axios';
// import checkAuth from '@/components/helpers/checkAuth';
const authAxios = axios.create({
  baseURL: import.meta.env.VITE_SERVE,
  withCredentials: true
});

authAxios.interceptors.response.use(
  (response) => response,
  (error) => {
    Promise.reject(error);
  },
);

export default authAxios;
