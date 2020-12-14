import React from 'react';
import { AppStateProvider } from '../state';
import { Route, Routes } from 'react-router';
import { Settings } from './Settings';
import ServicePage from './ServicePage';
import ServiceDetail from './ServiceDetail';
import ServiceList from './ServiceList';
import ServiceIssueList from './ServiceIssue/ServiceIssueList';
import { theZooClient, UrqlProvider } from 'zoo-api';

export const App = () => (
  <AppStateProvider>
    <UrqlProvider value={theZooClient}>
      <>
        <Routes>
          <Route path="/" element={<ServicePage />}>
            <Route path="/" element={<ServiceList />} />
            <Route path="/:id/:name/" element={<ServiceDetail />} />
            <Route path="/:id/:name/issues/" element={<ServiceIssueList />} />
          </Route>
        </Routes>
        <Settings />
      </>
    </UrqlProvider>
  </AppStateProvider>
);
