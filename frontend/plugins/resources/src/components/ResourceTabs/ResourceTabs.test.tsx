
import React from 'react';
import { render } from '@testing-library/react';
import mockFetch from 'jest-fetch-mock';
import ResourceTabs from './ResourceTabs';
import { ThemeProvider } from '@material-ui/core';
import { lightTheme } from '@backstage/theme';

describe('ResourceTabs', () => {
  it('should render', () => {
    mockFetch.mockResponse(() => new Promise(() => {}));
    const rendered = render(
      <ThemeProvider theme={lightTheme}>
        <ResourceTabs />
      </ThemeProvider>,
    );
    expect(rendered.getByText('Libraries')).toBeInTheDocument();
  });
});
