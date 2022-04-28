<script>
  import { createEventDispatcher, onMount } from 'svelte';
  import { Form, Message } from 'svelte-yup';

  import { applications, environments, envsFilteredByApp } from '../../store';
  import Dialog from '../../components/Dialog.svelte';
  import applicationService from '../../services/application_service';
  import environmentService from '../../services/environment_service';
  import { urlConfig } from '../../constants';

  export let open = false;
  export let selectedData;

  let submitted = false;
  let selected = [];
  let isValid;
  let envs = [];

  const dispatch = createEventDispatcher();

  onMount(() => {
    applicationService.get(urlConfig.application).then((data) => {
      applications.set(data);
    });

    environmentService.get(urlConfig.environment).then((data) => {
      environments.set(data);
    });
  });

  envsFilteredByApp.subscribe((data) => {
    envs = data;
  });

  const formSubmit = () => {
    isValid = true;

    if (isValid) {
      close({
        save: true,
        dataToSave: {
          application: selectedData.application,
          env: selected,
          image: selectedData.id,
        },
      });
    }
  };

  const close = (data) => {
    dispatch('close', data);
  };
</script>

<div class="modal">
  <Form class="form" submitHandler={formSubmit} {submitted}>
    <Dialog
      headerTxt="Deploy Image"
      {open}
      submitTxt="Deploy"
      on:close={close}
      on:submit={formSubmit}
    >
      {#each envs[selectedData.application] as data (data.id)}
        <input type="checkbox" bind:group={selected} value={data.id} />
        {data.env}<br />
      {/each}

      <Message name="environments" />
    </Dialog>
  </Form>
</div>

<style>
  :global(.modal-header) {
    background: #2d969b !important;
    color: white;
  }

  :global(.btnSave) {
    background: #2d969b;
  }

  :global(.form-control:focus) {
    box-shadow: 0 0 0 0.15rem #a0cbcd !important;
  }

  :global(.close-icon) {
    right: 8%;
    cursor: pointer;
    position: absolute;
    height: 25px;
  }

  :global(.close-icon svg) {
    color: #fff;
    stroke-width: 2px;
    width: 100% !important;
  }
</style>
