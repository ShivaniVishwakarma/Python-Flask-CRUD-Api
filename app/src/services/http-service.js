import { $axios } from '../common';

export class HttpService {
  get = (url) => {
    return $axios
      .get(url)
      .then((res) => res.data)
      .catch(this.catchException);
  };

  create = (url, data) => {
    return $axios
      .post(url, data)
      .then((res) => res.data)
      .catch(this.catchException);
  };

  update = (url, id, data) => {
    return $axios
      .put(`${url}${id}`, data)
      .then((res) => res.data)
      .catch(this.catchException);
  };

  deleteData = (url, id) => {
    return $axios
      .delete(`${url}${id}`)
      .then((res) => res.data)
      .catch(this.catchException);
  };

  catchException = (err) => {
    if (err.response?.data?.description) {
      alert(err.response.data.description);
    }

    return null;
  };
}
