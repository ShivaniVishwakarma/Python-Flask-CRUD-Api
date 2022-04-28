import { HttpService } from './http-service';
import { $axios } from '../common';
import { urlConfig } from '../constants';

class DeployService extends HttpService {
  deployVersion(data) {
    return $axios
      .put(`${urlConfig.deployment}deployVersion`, data)
      .then((res) => res.data)
      .catch(this.catchException);
  }
}

const deployService = new DeployService();

export default deployService;
