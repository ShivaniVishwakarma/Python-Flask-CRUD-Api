<script>
  import { createEventDispatcher } from 'svelte';
  import MdClose from 'svelte-icons/md/MdClose.svelte';

  import {
    Button,
    Modal,
    ModalBody,
    ModalFooter,
    ModalHeader,
  } from 'sveltestrap';

  export let open = false;
  export let headerTxt = '';
  export let submitTxt = '';

  const closeEvent = createEventDispatcher();
  const submitEvent = createEventDispatcher();

  function close() {
    closeEvent('close');
  }

  function submit() {
    submitEvent('submit');
  }
</script>

<div class="modal">
  <Modal isOpen={open} {close}>
    <ModalHeader {close} class="header"
      >{headerTxt}
      <icon on:click={close} class="close-icon"><MdClose /></icon>
    </ModalHeader>
    <ModalBody>
      <slot />
    </ModalBody>
    <ModalFooter>
      <Button class="submit-btn" on:click={submit}>{submitTxt}</Button>
      <Button color="secondary" on:click={close}>Cancel</Button>
    </ModalFooter>
  </Modal>
</div>

<style>
  :global(.modal-header) {
    background: #2d969b !important;
    color: white;
  }

  :global(.submit-btn) {
    background: #2d969b;
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
