
import React from 'react';
import { render } from '@testing-library/react';
import mockFetch from 'jest-fetch-mock';
import LanguagesPage from './LanguagesPage';
import { ThemeProvider } from '@material-ui/core';
import { lightTheme } from '@backstage/theme';

describe('LanguagesPage', () => {
  it('should render', () => {
    mockFetch.mockResponse(() => new Promise(() => {}));
    const rendered = render(
      <ThemeProvider theme={lightTheme}>
        <LanguagesPage />
      </ThemeProvider>,
    );
    expect(rendered.getByText('Welcome to language page!')).toBeInTheDocument();
  });
});
