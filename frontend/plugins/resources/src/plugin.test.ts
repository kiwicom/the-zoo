import { plugin } from './plugin';

describe('resources', () => {
  it('should export plugin', () => {
    expect(plugin).toBeDefined();
  });
});
