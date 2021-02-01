import React from 'react';
import { Route, Routes } from 'react-router';
import { theZooClient, UrqlProvider } from 'zoo-api';
import LanguagesPage from './LanguagesPage';
import LibrariesPage from './LibrariesPage';
import ResourcesPage from "./ResourcesPage";
import TemplatesPage from "./TemplatesPage";

export const App = () => (
    <UrqlProvider value={theZooClient}>
        <Routes>
          <Route path="/" element={<ResourcesPage />}>
            <Route path="languages" element={<LanguagesPage />} />
            <Route path="libraries" element={<LibrariesPage />}/>
            <Route path="ci_templates" element={<TemplatesPage />}/>
          </Route>
        </Routes>
    </UrqlProvider>
);

export const ResourcesTabsLabels = [
  { id: 0, label: 'Languages', route: 'languages' },
  { id: 1, label: 'Libraries', route: 'libraries' },
  { id: 2, label: 'CI/CD Templates', route: 'ci_templates' }
];
