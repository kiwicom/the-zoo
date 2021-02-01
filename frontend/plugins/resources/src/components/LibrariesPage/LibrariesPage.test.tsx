
import React from 'react';
import { render } from '@testing-library/react';
import mockFetch from 'jest-fetch-mock';
import LibrariesPage from './LibrariesPage';
import { ThemeProvider } from '@material-ui/core';
import { lightTheme } from '@backstage/theme';

describe('LibrariesPage', () => {
  it('should render', () => {
    mockFetch.mockResponse(() => new Promise(() => {}));
    const rendered = render(
      <ThemeProvider theme={lightTheme}>
        <LibrariesPage />
      </ThemeProvider>,
    );
    expect(rendered.getByText('Welcome to libraries page!')).toBeInTheDocument();
  });
});
