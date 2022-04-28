<script>
  import Router from 'svelte-spa-router';
  import { wrap } from 'svelte-spa-router/wrap';

  import { setAxiosConfig } from './common';

  import AppHeader from './components/AppHeader.svelte';
  import ApplicationPage from './pages/application/ApplicationPage.svelte';
  import EnvironmentPage from './pages/environment/EnvironmentPage.svelte';
  import ImagePage from './pages/image/ImagePage.svelte';
  import DeployPage from './pages/deploy/DeployPage.svelte';

  let apiUrl;

  if (process.env['isProd']) {
    console.log('running production');
    apiUrl = `http://${window.location.hostname}:5000`;
  } else {
    apiUrl = process.env['apiUrl'];
  }

  console.log('apiUrl ', apiUrl);
  setAxiosConfig(apiUrl, 5000);
</script>

<svelte:head>
  <base href="/#" />
</svelte:head>

<main>
  <AppHeader />
  <Router
    routes={{
      '/application': ApplicationPage,
      '/env': wrap({
        asyncComponent: () =>
          import('./pages/environment/EnvironmentPage.svelte'),
      }),
      '/image': wrap({
        asyncComponent: () => import('./pages/image/ImagePage.svelte'),
      }),
      '/deployment': DeployPage,
      '*': ApplicationPage,
    }}
  />
</main>
