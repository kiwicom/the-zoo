
import React from 'react';
import { render } from '@testing-library/react';
import mockFetch from 'jest-fetch-mock';
import TemplatesPage from './TemplatesPage';
import { ThemeProvider } from '@material-ui/core';
import { lightTheme } from '@backstage/theme';

describe('TemplatesPage', () => {
  it('should render', () => {
    mockFetch.mockResponse(() => new Promise(() => {}));
    const rendered = render(
      <ThemeProvider theme={lightTheme}>
        <TemplatesPage />
      </ThemeProvider>,
    );
    expect(rendered.getByText('Welcome to Ci templates page!')).toBeInTheDocument();
  });
});
