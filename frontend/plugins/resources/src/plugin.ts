import { createPlugin, createRouteRef } from '@backstage/core';
// import ExampleComponent from './components/ExampleComponent';
import { App } from './components/App';

export const rootRouteRef = createRouteRef({
  path: 'resources/*',
  title: 'resources',
});

export const plugin = createPlugin({
  id: 'resources',
  register({ router }) {
    router.addRoute(rootRouteRef, App);
  },
});
