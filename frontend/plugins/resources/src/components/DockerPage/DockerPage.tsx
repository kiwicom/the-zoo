import React from 'react';
import { Content, Page, Table } from '@backstage/core';
import {Connection, Dependency, getDependencies, unwrap, useBackend} from 'zoo-api';
import { Grid } from '@material-ui/core';
import { generateTableData, commonColumns } from '../TableComponents/TableData'


const DockerPage = () => {
  const [response, component] = useBackend<Connection<Dependency>>("dependencies", getDependencies, {type: ["Docker Image"]});

  if (component) return <Grid item>{component}</Grid>;
  if (!response) return null;
  const deps = unwrap<Dependency>(response);
  const dockerData = generateTableData(deps);

  return (
    <Page themeId="home">
      <Content>
        <div>
          <Table
            options={{ paging: true, padding: 'default' }}
            data={dockerData}
            columns={commonColumns}
          />
        </div>
      </Content>
    </Page>
  )
};

export default DockerPage;
