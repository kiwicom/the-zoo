import React from 'react';
import { Content, Page, Table } from '@backstage/core';
import {Connection, Dependancy, getDependencies, unwrap, useBackend} from 'zoo-api';
import { Grid } from '@material-ui/core';
import { generateTableData, commonColumns } from '../TableComponents/TableData'


const TemplatesPage = () => {
  const [response, component] = useBackend<Connection<Dependancy>>("dependencies", getDependencies, {type: ["Gitlab-ci.yml"]});

  if (component) return <Grid item>{component}</Grid>;
  if (!response) return null;
  const deps = unwrap<Dependancy>(response);
  const templateData = generateTableData(deps);

  return (
    <Page themeId="home">
      <Content>
        <div>
          <Table
            options={{ paging: true, padding: 'default' }}
            data={templateData}
            columns={commonColumns}
          />
        </div>
      </Content>
    </Page>
  )
};

export default TemplatesPage;
