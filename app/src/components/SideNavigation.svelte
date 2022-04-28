<script>
  import { Link } from 'svelte-routing';
  import MdClose from 'svelte-icons/md/MdClose.svelte';
  import { createEventDispatcher } from 'svelte';

  export let width = '0px';

  let src = 'rollout-logo.jpg';

  const dispatch = createEventDispatcher();
  function close() {
    dispatch('changeWidth', true);
  }
</script>

<div class="sidebar" style="width: {width};">
  <span class="close" on:click={close}><MdClose /></span>

  <div class="profile">
    <h1
      style="width: 270px;
      color: white;
      font-style: italic;
      margin-bottom: 3.2rem;
      padding: 15px;"
    >
      Rollout Manager
    </h1>
  </div>

  <nav on:click={close} class="nav">
    <a href="#/application">Application</a>
    <a href="#/env">Environment</a>
    <a href="#/image">Image</a>
    <a href="#/deployment">Deployment</a>
  </nav>
</div>

<style>
  .close {
    cursor: pointer;
  }

  .close :global(svg) {
    color: white;
    stroke-width: 2px;
  }

  .nav > :global(a) {
    color: white;
    padding: 15px 30px;
  }

  .nav > :global(a:link) {
    text-decoration: none;
  }

  .nav > :global(a:visited) {
    text-decoration: none;
  }

  .nav > :global(a:hover) {
    text-decoration: none;
    background: #3fa6ab;
  }

  .nav > :global(a:active) {
    text-decoration: none;
  }

  .sidebar {
    height: 100%;
    position: fixed;
    top: 0;
    left: 0;
    z-index: 1;
    padding-top: 15px;
    background: #2d969b;
    user-select: none;
    transition: 0.5s ease;
    overflow-x: hidden;
  }

  .profile {
    text-align: center;
    font-size: 15px;
    margin-top: 41px;
    color: white;
  }
  nav {
    display: flex;
    flex-direction: column;
    margin-top: 30px;
  }
</style>
