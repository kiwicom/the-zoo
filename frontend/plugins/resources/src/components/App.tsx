import React from 'react';
import { Route, Routes } from 'react-router';
import { theZooClient, UrqlProvider } from 'zoo-api';
import LanguagesPage from './LanguagesPage';
import LibrariesPage from './LibrariesPage';
import ResourcesPage from './ResourcesPage';
import TemplatesPage from './TemplatesPage';
import Detailpage from './DetailPage';

export const App = () => (
    <UrqlProvider value={theZooClient}>
        <Routes>
          <Route path="/" element={<ResourcesPage />}>
            <Route path="/" element={<LibrariesPage />}/>
            <Route path="languages" element={<LanguagesPage />} />
            <Route path="libraries" element={<LibrariesPage />}/>
            <Route path="ci_templates" element={<TemplatesPage />}/>
          </Route>
          <Route path="dependencies/:id" element={<Detailpage />}/>
        </Routes>
    </UrqlProvider>
);

export const ResourcesTabsLabels = [
  { id: 0, label: 'Libraries', route: 'libraries' },
  { id: 1, label: 'Languages', route: 'languages' },
  { id: 2, label: 'CI/CD Templates', route: 'ci_templates' }
];
