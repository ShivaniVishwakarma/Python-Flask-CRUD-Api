import { writable, derived } from 'svelte/store';

/** Store for your data. 
This assumes the data you're pulling back will be an array.
If it's going to be an object, default this to an empty object.
**/
export const applications = writable([]);
export const environments = writable([]);
export const images = writable([]);
export const deployments = writable([]);

export const appNames = derived(applications, ($applications) => {
  return $applications.map((x) => {
    return { value: x.name, key: x.id };
  });
});

export const envsFilteredByApp = derived(
  [applications, environments],
  ([$applications, $environments]) => {
    if ($applications.length == 0 && $environments.length == 0) return [];

    var result = {};

    $applications.map((x) => {
      const envs = $environments.filter((y) => y.application == x.id);
      result[x.id] = envs;
    });

    return result;
  }
);
