import React from 'react';
import { AppStateProvider } from '../state';
import { Route, Routes } from 'react-router';
import { Settings } from './Settings';
import ServicePage from './ServicePage';
import ServiceDetail from './ServiceDetail';
import ServiceList from './ServiceList';
import ServiceIssueDetail from './ServiceIssueDetail';
import ServiceIssueList from './ServiceIssueList';
import { theZooClient, UrqlProvider } from 'zoo-api';

export const App = () => (
  <AppStateProvider>
    <UrqlProvider value={theZooClient}>
      <>
        <Routes>
          <Route path="/" element={<ServicePage />}>
            <Route path="/" element={<ServiceList />} />
            <Route path="/:name/" element={<ServiceDetail />} />
            <Route path="/:name/issues/" element={<ServiceIssueList />} />
            <Route path="/:name/issuse/:id/" element={<ServiceIssueDetail />} />
          </Route>
        </Routes>
        <Settings />
      </>
    </UrqlProvider>
  </AppStateProvider>
);
