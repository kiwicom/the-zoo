
import StorageIcon from '@material-ui/icons/Storage';
import { createPlugin, createRouteRef } from '@backstage/core';
import { App } from './components/App';

export const rootRouteRef = createRouteRef({
  icon: StorageIcon,
  path: '/services/*',
  title: 'services',
});

export const plugin = createPlugin({
  id: 'services',
  register({ router }) {
    router.addRoute(rootRouteRef, App);
  },
});
