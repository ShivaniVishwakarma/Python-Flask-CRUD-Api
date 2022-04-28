<script>
  // icons
  import FaBars from 'svelte-icons/fa/FaBars.svelte';

  import Hamburger from './SideNavigation.svelte';

  let width = '0px';

  function changeWidth() {
    width = width === '300px' ? '0px' : '300px';
  }
</script>

<nav>
  <ul style="width: 100%;display: flex;align-items: center;">
    <li>
      <span
        style="left: -45px;
        position: relative;"
        on:click={changeWidth}><FaBars /></span
      >
    </li>
  </ul>

  <Hamburger {width} on:changeWidth={changeWidth} />
</nav>

<style>
  li {
    display: inline;
    float: left;
  }

  nav {
    background: #2d969b;
    display: flex;
    align-items: center;
    justify-content: flex-start;
    height: 3em;
  }

  span {
    height: 20px;
    display: block;
    flex: 1;
    cursor: pointer;
  }

  ::placeholder {
    color: white;
    opacity: 1; /* Firefox */
  }

  :global(svg) {
    transform: translate(25px);
    color: white;
    width: 20px !important;
  }
</style>
