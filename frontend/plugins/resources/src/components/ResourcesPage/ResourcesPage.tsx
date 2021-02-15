import React from 'react';
import { Outlet } from 'react-router-dom';
import { Content, Page } from '@backstage/core';
import ResourceTabs from '../ResourceTabs';
import ResourcesHeader from '../ResourcesHeader'

const ResourcesPage = () => (
  <Page themeId="home">
    <ResourcesHeader title="Kiwi.com resources" description="Libraries, Languages, CI templates" />
    <ResourceTabs />
    <Content>
      <Outlet />
    </Content>
  </Page>
);

export default ResourcesPage;
