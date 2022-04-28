import createAuth0client from '@auth0/auth0-spa-js';
import config from '../config/auth_config';
import { user, isAuthenticated, popupOpen } from '../config/store';

async function createClient() {
  let auth0Client = await createAuth0client({
    domain: config.domain,
    client_id: config.clientId,
  });

  return auth0Client;
}

async function loginWithPopup(client, options) {
  popupOpen.set(true);

  try {
    await client.loginWithPopup(options);

    const token = await client.getTokenSilently();
    localStorage.setItem('token', token);

    user.set(await client.getUser());
    isAuthenticated.set(true);
  } catch (e) {
    console.log(e);
  } finally {
    popupOpen.set(false);
  }
}

function logout(client) {
  return client.logout();
}

const auth = { createClient, loginWithPopup, logout };

export default auth;
