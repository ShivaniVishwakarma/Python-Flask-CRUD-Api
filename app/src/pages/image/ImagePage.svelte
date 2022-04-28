<script lang="ts">
  import { onMount } from 'svelte';
  import { dayjs } from 'svelte-time';
  import { Alert, Button, Card } from 'sveltestrap';

  import imageService from '../../services/image_service';
  import environmentService from '../../services/environment_service';
  import appService from '../../services/application_service';
  import deployService from '../../services/deploy_service';

  import { environments, images, applications } from '../../store';
  import ImageDialog from './ImageDialog.svelte';
  import { urlConfig } from '../../constants';

  let open = false;
  let selectedData;

  onMount(() => {
    appService.get(urlConfig.application).then((data) => {
      applications.set(data);
    });

    imageService.get(urlConfig.image).then((data) => {
      images.set(data);
    });

    environmentService.get(urlConfig.environment).then((data) => {
      environments.set(data);
    });
  });

  let alertMessage = '';

  const submit = (data) => {
    alertMessage = '';
    if (data.detail?.save) {
      deployService.deployVersion(data.detail.dataToSave).then((res) => {
        if (res) {
          alertMessage = 'Version deployed successfully.';

          setTimeout(() => {
            alertMessage = '';
          }, 2000);
        }
      });
    }

    toggleDialog();
  };

  const toggleDialog = (data = undefined) => {
    open = !open;

    if (open) {
      selectedData = data;
    }
  };

  let columns = ['Application', 'Image', 'Created At', 'Actions'];
</script>

<Card body class="container">
  <h1>Images</h1>

  <table class="table">
    <thead>
      <tr>
        {#each columns as column (column)}
          <th scope="col">{column}</th>
        {/each}
      </tr>
    </thead>
    <tbody>
      {#each $images as image (image.id)}
        <tr style="height: 10px;">
          <td>{image.appName}</td>
          <td>{image.image}</td>
          <td>{dayjs(image.createdDate).format('MMM DD, YYYY HH:mm:ss')}</td>

          <td>
            <Button color="success" on:click={() => toggleDialog(image)}
              >Deploy</Button
            >
            <Button color="danger" disabled={true}>Delete</Button>
          </td>
        </tr>
      {/each}
    </tbody>
  </table>
</Card>

<Alert color="success" isOpen={!!alertMessage}>
  {alertMessage}
</Alert>

{#if open}
  <ImageDialog on:close={submit} {open} {selectedData} />
{/if}

<style>
  table :global(.btn) {
    font-size: 12px;
  }
</style>
