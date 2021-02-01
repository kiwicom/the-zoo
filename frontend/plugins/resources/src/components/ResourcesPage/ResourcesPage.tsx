import React from 'react';
import { Outlet } from 'react-router-dom';
import { Content, Header, HeaderLabel, Page } from '@backstage/core';
import ResourceTabs from '../ResourceTabs';

const ResourcesPage = () => (
  <Page themeId="home">
    <Header title="Kiwi.com resources" subtitle="Libraries, Languages, CI templates">
      <HeaderLabel label="Owner" value="Platform Software Squad" />
      <HeaderLabel label="Lifecycle" value="Alpha" />
    </Header>
    <ResourceTabs />

    <Content>

      <Outlet />

    </Content>
  </Page>
);

export default ResourcesPage;
