import { createPlugin } from '@backstage/core'
import ExampleComponent from './components/ExampleComponent'

export const plugin = createPlugin({
  id: 'services',
  register({ router }) {
    router.registerRoute('/services', ExampleComponent)
  },
})
