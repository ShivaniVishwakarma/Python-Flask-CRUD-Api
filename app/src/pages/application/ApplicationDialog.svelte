<script>
  import { createEventDispatcher } from 'svelte';
  import { Form, Message, isInvalid } from 'svelte-yup';
  import { FormGroup, Input, Label } from 'sveltestrap';
  import * as yup from 'yup';

  import Dialog from '../../components/Dialog.svelte';

  let schema = yup.object().shape({
    name: yup.string().required().label('Name'),
    gitRepo: yup.string().required().url().label('Git repository url'),
  });

  export let open = false;
  let submitted = false;
  let isValid;

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

  export let isEditMode = false;
  export let fields = { name: '', gitRepo: '' };

  $: invalid = (name) => {
    if (submitted) {
      return isInvalid(schema, name, fields);
    }
    return false;
  };
</script>

<div class="modal">
  <Form class="form" {schema} {fields} submitHandler={formSubmit} {submitted}>
    <Dialog
      headerTxt="{isEditMode ? 'Update' : 'Create'} Application"
      {open}
      submitTxt={isEditMode ? 'Update' : 'Save'}
      on:close={close}
      on:submit={formSubmit}
    >
      <FormGroup>
        <Label>Application Name</Label>
        <Input
          type="text"
          id="name"
          class="form-control"
          bind:value={fields.name}
        />
        <Message name="name" />
      </FormGroup>
      <FormGroup>
        <Label>Git Url</Label>
        <Input
          id="gitRepo"
          type="text"
          class="form-control"
          bind:value={fields.gitRepo}
        />
        <Message name="gitRepo" />
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
