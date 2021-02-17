
import React from 'react';
import { render } from '@testing-library/react';
import mockFetch from 'jest-fetch-mock';
import DockerPage from './DockerPage';
import { ThemeProvider } from '@material-ui/core';
import { lightTheme } from '@backstage/theme';

describe('DockerPage', () => {
  it('should render', () => {
    mockFetch.mockResponse(() => new Promise(() => {}));
    const rendered = render(
      <ThemeProvider theme={lightTheme}>
        <DockerPage />
      </ThemeProvider>,
    );
    expect(rendered.getByText('Welcome to Docker images page!')).toBeInTheDocument();
  });
});
