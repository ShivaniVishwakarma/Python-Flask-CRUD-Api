<script lang="ts">
  import { onMount } from 'svelte';
  import { Alert, Card } from 'sveltestrap';
  import { dayjs } from 'svelte-time';
  import MdAdd from 'svelte-icons/md/MdAdd.svelte';

  import { applications } from '../../store';

  import applicationService from '../../services/application_service';

  import ApplicationDialog from './ApplicationDialog.svelte';

  import { urlConfig } from '../../constants';
  import Table from '../../components/Table.svelte';

  let apps = [];
  let open = false;
  let application = { name: '', gitRepo: '' };
  let isEditMode = false;
  const toggle = () => (open = !open);
  let alertMessage = '';

  onMount(() => {
    applicationService.get(urlConfig.application).then((data) => {
      const result = data.map((x) => {
        x.createdDate = dayjs(x.createdDate).format('MMM DD, YYYY HH:mm:ss');
        return x;
      });
      applications.set(result);
    });
  });

  applications.subscribe((value) => (apps = value));

  function dialogClose({ detail }) {
    if (detail && detail.data.save) {
      const {
        data: { dataToSave },
      } = detail;

      if (isEditMode) {
        applicationService
          .update(urlConfig.application, dataToSave.id, dataToSave)
          .then((data) => {
            if (data) {
              const itemToUpdateIndex = apps.findIndex(
                (x) => x.id === dataToSave.id
              );

              if (itemToUpdateIndex > -1) {
                apps[itemToUpdateIndex] = data;
              }

              updateStore();
              showAlert('Data updated succesfully.');
            }
          });
      } else {
        applicationService
          .create(urlConfig.application, dataToSave)
          .then((data) => {
            if (data) {
              apps.push(data);

              updateStore();
              showAlert('Data created succesfully.');
            }
          });
      }
    }

    open = false;
    isEditMode = false;
  }

  function updateStore() {
    applications.set(apps);
  }

  function editRow(event) {
    application = event.detail;
    isEditMode = true;
    open = true;
  }

  function removeRow(event) {
    const id = event.detail;
    applicationService.deleteData(urlConfig.application, id).then((data) => {
      if (data) {
        const itemToDeleteIndex = apps.findIndex((x) => x.id === id);

        if (itemToDeleteIndex > -1) {
          apps.splice(itemToDeleteIndex, 1);
        }

        updateStore();
        showAlert('Data deleted successfully');
      }
    });
  }

  function showAlert(message) {
    alertMessage = message;
    setTimeout(() => {
      alertMessage = '';
    }, 2000);
  }

  let columns = ['Id', 'Name', 'Git Repo Url', 'Created Date'];
  let fields = ['id', 'name', 'gitRepo', 'createdDate'];
</script>

<Card body>
  <h1>Applications</h1>

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
    rows={apps}
  />
</Card>

<ApplicationDialog
  on:close={dialogClose}
  {open}
  fields={application}
  {isEditMode}
/>
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

  :global(svg) {
    color: black;
  }
  .create :global(svg) {
    color: #fff;
    float: left;
    margin-top: 1px;
    stroke-width: 2px;
  }
</style>
