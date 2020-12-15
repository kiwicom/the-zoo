import React from 'react';
import { Outlet } from 'react-router-dom';
import { Content, Header, HeaderLabel, Page } from '@backstage/core';

const ServicePage = () => (
  <Page themeId="home">
    <Header title="Kiwi.com services" subtitle="Most of them aren’t microservices to be honest">
      <HeaderLabel label="Owner" value="Platform Software Squad" />
      <HeaderLabel label="Lifecycle" value="Alpha" />
    </Header>
    <Content>

      <Outlet />

    </Content>
  </Page>
);

export default ServicePage;
