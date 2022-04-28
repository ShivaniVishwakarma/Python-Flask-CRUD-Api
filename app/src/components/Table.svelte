<script>
  import { createEventDispatcher } from 'svelte';
  import MdDelete from 'svelte-icons/md/MdDelete.svelte';
  import MdEdit from 'svelte-icons/md/MdEdit.svelte';

  export let columns = [];
  export let rows = [];
  export let fields = [];

  const event = createEventDispatcher();

  export const remove = (id) => {
    event('remove', id);
  };
  export const edit = (data) => {
    event('edit', data);
  };
</script>

<table class="table">
  <thead>
    <tr>
      {#each columns as column (column)}
        <th scope="col">{column}</th>
      {/each}

      <th scope="col">Actions</th>
    </tr>
  </thead>
  <tbody>
    {#each rows as row (row.id)}
      <tr>
        {#each fields as field (field)}
          <td>{row[field]}</td>
        {/each}

        <td>
          <icon on:click={() => remove(row.id)}><MdDelete /></icon>
          <icon on:click={() => edit(row)}><MdEdit /></icon>
        </td>
      </tr>
    {/each}
  </tbody>
</table>

<style>
  icon {
    cursor: pointer;
  }
</style>