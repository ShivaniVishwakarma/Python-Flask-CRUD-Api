<script>
  import { isAuthenticated, user, tasks, user_tasks } from '../config/store';

  let newTask;

  function addItem() {
    let newTaskObject = {
      id: genRandom(),
      description: newTask,
      completed: false,
      user: $user.email,
    };

    let updatedTasks = [...$tasks, newTaskObject];

    tasks.set(updatedTasks);

    newTask = '';
  }

  function genRandom(length = 7) {
    var chars =
      '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ';
    var result = '';
    for (var i = length; i > 0; --i)
      result += chars[Math.round(Math.random() * (chars.length - 1))];
    return result;
  }
</script>

<div>
  <a href="/#">Task Manager</a>

  <div class="collapse navbar-collapse" id="navbarText">
    <div class="navbar-nav mr-auto user-details">
      {#if $isAuthenticated}
        <span style="color:black">&nbsp;&nbsp;{$user.name} ({$user.email})</span
        >
      {:else}<span>&nbsp;</span>{/if}
    </div>
    <span class="navbar-text">
      <ul class="navbar-nav float-right">
        {#if $isAuthenticated}
          <li class="nav-item">
            <a class="nav-link" href="/#" on:click={logout}>Log Out</a>
          </li>
        {:else}
          <li class="nav-item">
            <a class="nav-link" href="/#" on:click={login}>Log In</a>
          </li>
        {/if}
      </ul>
    </span>
  </div>
</div>
