import React from 'react';
import { Content, Page, Table, TableColumn, TableFilter } from '@backstage/core';
import { getDependencies, Dependency, unwrap, useBackend, Connection } from 'zoo-api';
import { Chip, Grid } from "@material-ui/core";
import ResourceKind from "../TableComponents/ResourceKind";
import ResourceTypeLabel from "../TableComponents/ResourceTypeLabel";
import ResourceLink from "../TableComponents/ResourceLink";
import { generateTableData } from '../TableComponents/TableData';


const columns: TableColumn[] = [
  {
    title: 'Usage',
    field: 'usage',
    type: 'numeric',
    highlight: true,
  },
  {
    title: 'Name',
    field: 'name',
    type: 'string',
    render: (rowData:object) => <ResourceLink name={rowData.name} id={rowData.id} />
  },
  {
    title: 'Latest Version',
    field: 'version',
    render: (rowData:object) => <Chip label={rowData.version} />
  },
  {
    title: 'Type',
    field: 'type',
    render: (rowData:object) => <ResourceTypeLabel name={rowData.type} />
  },
  {
    title: 'Kind',
    field: 'kind',
    render: (rowData:object) => <ResourceKind name={rowData.name} />
  },
];

const filters: TableFilter[] = [
  {
    column: 'Kind',
    type: 'select',
  }
];

const LibrariesPage = () => {
  const [response, component] = useBackend<Connection<Dependency>>("dependencies", getDependencies, {type: ["Python Library", "Javascript Library"]});

  if (component) return <Grid item>{component}</Grid>;
  if (!response) return null;

  const deps = unwrap<Dependency>(response);
  const libraryData = generateTableData(deps);

  return (
    <Page themeId="home">
      <Content>
        <div>
          <Table
            options={{ paging: true, padding: 'default' }}
            data={libraryData}
            columns={columns}
            filters={filters}
          />
        </div>
      </Content>
    </Page>
  )
};

export default LibrariesPage;
