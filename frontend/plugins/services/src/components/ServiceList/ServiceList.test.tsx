
import React from 'react';
import { render } from '@testing-library/react';
import mockFetch from 'jest-fetch-mock';
import ServiceList from './ServiceList';

describe('ServiceList', () => {
  it('should render', async () => {
    mockFetch.mockResponse(() => new Promise(() => {}));
    const rendered = render(<ServiceList />);
    expect(await rendered.findByTestId('progress')).toBeInTheDocument();
  });
});
