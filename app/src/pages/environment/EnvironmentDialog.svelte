<script>
  import { createEventDispatcher, onMount } from 'svelte';
  import { Form, Message, isInvalid } from 'svelte-yup';
  import { FormGroup, Input, Label } from 'sveltestrap';
  import * as yup from 'yup';

  import applicationService from '../../services/application_service';

  import { applications, appNames } from '../../store';

  import Dialog from '../../components/Dialog.svelte';

  import { urlConfig } from '../../constants';

  let schema = yup.object().shape({
    application: yup.string().required().label('Application'),
    env: yup.string().required().label('Environment'),
    path: yup.string().required().label('Path'),
  });

  export let open = false;
  export let isEditMode = false;
  export let environment;

  let fields = environment
    ? { ...environment }
    : { env: '', application: '', path: '' };

  let submitted = false;
  let isValid;

  onMount(() => {
    applicationService.get(urlConfig.application).then((data) => {
      applications.set(data);
    });
  });

  const dispatch = createEventDispatcher();

  function formSubmit() {
    submitted = true;

    isValid = schema.isValidSync(fields);
    if (isValid) {
      close({ save: true, dataToSave: fields });
    }
  }

  function close(data) {
    dispatch('close', {
      data,
    });
  }
</script>

<div class="modal">
  <Form class="form" {schema} {fields} submitHandler={formSubmit} {submitted}>
    <Dialog
      headerTxt="{isEditMode ? 'Update' : 'Create'} Environment"
      {open}
      submitTxt={isEditMode ? 'Update' : 'Save'}
      on:close={close}
      on:submit={formSubmit}
    >
      <FormGroup>
        <Label for="application">App</Label>
        <Input
          type="select"
          name="select"
          id="application"
          bind:value={fields.application}
        >
          <option value="" />
          {#each $appNames as application}
            <option
              value={application.key}
              selected={fields.application == application.key}
              >{application.value}
            </option>
          {/each}
        </Input>
        <Message name="application" />
      </FormGroup>
      <FormGroup>
        <Label>Environment Name</Label>
        <Input
          type="text"
          id="name"
          class="form-control"
          bind:value={fields.env}
        />
        <Message name="name" />
      </FormGroup>
      <FormGroup>
        <Label>Path</Label>
        <Input
          id="path"
          type="text"
          class="form-control"
          bind:value={fields.path}
        />
        <Message name="path" />
      </FormGroup>
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

  :global(.modal-dialog) {
    transform: translate(0, 50%) !important;
  }
</style>
