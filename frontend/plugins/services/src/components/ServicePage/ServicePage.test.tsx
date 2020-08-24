
import React from 'react';
import { render } from '@testing-library/react';
import mockFetch from 'jest-fetch-mock';
import ServicePage from './ServicePage';
import { ThemeProvider } from '@material-ui/core';
import { lightTheme } from '@backstage/theme';

describe('ServicePage', () => {
  it('should render', () => {
    mockFetch.mockResponse(() => new Promise(() => {}));
    const rendered = render(
      <ThemeProvider theme={lightTheme}>
        <ServicePage />
      </ThemeProvider>,
    );
    expect(rendered.getByText('Welcome to services!')).toBeInTheDocument();
  });
});
