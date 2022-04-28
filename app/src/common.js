import 'bootstrap/dist/css/bootstrap.min.css';
import './styles.css';

import axios from 'axios';

export let $axios;
export const setAxiosConfig = (url, timeout) => {
  const config = {
    baseURL: url,
    timeout,
  };

  console.log('axios config', config);
  $axios = axios.create(config);
};
