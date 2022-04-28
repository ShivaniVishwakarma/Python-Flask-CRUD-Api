<script lang="ts">
  import { onMount } from 'svelte';
  import { dayjs } from 'svelte-time';

  import { Card } from 'sveltestrap';
  import { urlConfig } from '../../constants';

  import deployService from '../../services/deploy_service';
  import { deployments } from '../../store';

  onMount(() => {
    deployService.get(urlConfig.deployment).then((data) => {
      deployments.set(data);
    });
  });
</script>

<Card body class="container">
  <h1>Deployments</h1>

  <table class="table">
    <thead>
      <tr>
        <th scope="col">Application</th>
        <th scope="col">Image</th>
        <th scope="col">Environment</th>
        <th scope="col">Deployed At</th>
      </tr>
    </thead>
    <tbody>
      {#each $deployments as deployment (deployment.id)}
        <tr style="height: 10px;">
          <td>{deployment.application}</td>
          <td>{deployment.image}</td>
          <td>{deployment.env}</td>
          <td
            >{deployment.createdDate
              ? dayjs(deployment.createdDate).format('MMM DD, YYYY HH:mm:ss')
              : ''}</td
          >
        </tr>
      {/each}
    </tbody>
  </table>
</Card>

<style>
  table :global(.btn) {
    font-size: 12px;
  }
</style>
