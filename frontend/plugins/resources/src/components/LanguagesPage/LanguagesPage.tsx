import React from 'react';
import { Content, Page, Table } from '@backstage/core';
import { Dependency, getDependencies, unwrap, useBackend, Connection } from 'zoo-api';
import { Grid } from '@material-ui/core';
import { generateTableData, commonColumns } from '../TableComponents/TableData'


const LanguagesPage = () => {
  const [response, component] = useBackend<Connection<Dependency>>("dependencies", getDependencies, {type: ["Language"]});

  if (component) return <Grid item>{component}</Grid>;
  if (!response) return null;

  const deps = unwrap<Dependency>(response);
  const languagesData = generateTableData(deps);

  return (
    <Page themeId="home">
      <Content>
        <div>
          <Table
            options={{ paging: true, padding: 'default' }}
            data={languagesData}
            columns={commonColumns}
          />
        </div>
      </Content>
    </Page>
  );
};

export default LanguagesPage;
