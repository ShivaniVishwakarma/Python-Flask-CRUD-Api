<script lang="ts">
  import { onMount } from 'svelte';
  import MdAdd from 'svelte-icons/md/MdAdd.svelte';
  import MdDelete from 'svelte-icons/md/MdDelete.svelte';
  import MdEdit from 'svelte-icons/md/MdEdit.svelte';

  import { Alert, Card } from 'sveltestrap';
  import { environments } from '../../store';
  import environmentService from '../../services/environment_service';
  import EnvironmentDialog from './EnvironmentDialog.svelte';
  import { urlConfig } from '../../constants';
  import Table from '../../components/Table.svelte';

  onMount(() => {
    environmentService.get(urlConfig.environment).then((data) => {
      environments.set(data);
    });
  });

  let envs = [];
  let open = false;
  let environment = { env: '', application: '', path: '' };
  let isEditMode = false;
  let alertMessage;

  const toggle = () => (open = !open);
  environments.subscribe((value) => (envs = value));

  function dialogClose({ detail }) {
    if (detail && detail.data.save) {
      const {
        data: { dataToSave },
      } = detail;

      if (isEditMode) {
        environmentService
          .update(urlConfig.environment, dataToSave.id, dataToSave)
          .then((data) => {
            const itemToUpdateIndex = envs.findIndex(
              (x) => x.id === dataToSave.id
            );

            if (itemToUpdateIndex > -1) {
              envs[itemToUpdateIndex] = data;
            }

            updateStore();
            showAlert('Data updated succesfully.');
          });
      } else {
        environmentService
          .create(urlConfig.environment, dataToSave)
          .then((data) => {
            if (data) {
              envs.push(data);
              updateStore();
              showAlert('Data created succesfully.');
            }
          });
      }
    }

    environment = null;
    open = false;
    isEditMode = false;
  }

  function updateStore() {
    environments.set(envs);
  }

  function showAlert(message) {
    alertMessage = message;
    setTimeout(() => {
      alertMessage = '';
    }, 2000);
  }

  function editRow(data) {
    environment = data.detail;
    isEditMode = true;
    open = true;
  }

  function removeRow(dataToRemove) {
    const id = dataToRemove.detail;
    environmentService.deleteData(urlConfig.environment, id).then((data) => {
      if (data) {
        const itemToDeleteIndex = envs.findIndex((x) => x.id === id);

        if (itemToDeleteIndex > -1) {
          envs.splice(itemToDeleteIndex, 1);
        }

        updateStore();
        showAlert('Data deleted successfully');
      }
    });
  }

  environments.subscribe((data) => (envs = data));

  let columns = ['Id', 'Name', 'Application', 'Path'];
  let fields = ['id', 'env', 'appName', 'path'];
</script>

<Card body>
  <h1>Environments</h1>

  <div>
    <button class="create" on:click={toggle}>
      <span> <MdAdd /> Create</span></button
    >
  </div>

  <Table
    {fields}
    {columns}
    on:remove={removeRow}
    on:edit={editRow}
    rows={envs}
  />

  {#if open}
    <EnvironmentDialog
      on:close={dialogClose}
      {open}
      {environment}
      {isEditMode}
    />
  {/if}
</Card>

<Alert color="success" isOpen={!!alertMessage}>
  {alertMessage}
</Alert>

<style>
  div {
    margin: 10px;
  }

  .create {
    background: #2d969b;
    color: white;
    width: 150px;
    border-radius: 5px;
    cursor: pointer;
  }

  .create :global(svg) {
    color: #fff;
    float: left;
    margin-top: 1px;
    stroke-width: 2px;
  }

  :global(svg) {
    color: black;
  }
</style>
