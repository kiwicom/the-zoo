import React from 'react';
import { Content, Page, Table, TableColumn, TableFilter } from '@backstage/core';
import { getResources, DummyResponse, Resource, unwrap } from 'zoo-api';
// import {useQuery} from "urql";
import { Chip, Grid } from "@material-ui/core";
import Alert from '@material-ui/lab/Alert';

import ResourceKind from "../TableComponents/ResourceKind";
import ResourceTypeLabel from "../TableComponents/ResourceTypeLabel";
import ResourceLink from "../TableComponents/ResourceLink";


const generateTableData: (resources: Resource[]) => Array<{}> = (resources) => {
  return resources.map(item => {
    return {
      id: item.id,
      usage: item.usageCount,
      name: item.name,
      version: item.version,
      type: item.type,
      kind: item.name,
    }
  });
};

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
    render: rowData => <ResourceLink name={rowData.name} id={rowData.id} />
  },
  {
    title: 'Latest Version',
    field: 'version',
    render: rowData => <Chip label={rowData.version} />
  },
  {
    title: 'Type',
    field: 'type',
    render: rowData => <ResourceTypeLabel name={rowData.type} />
  },
  {
    title: 'Kind',
    field: 'kind',
    render: rowData => <ResourceKind name={rowData.name} />
  },
];

const filters: TableFilter[] = [
  {
    column: 'Kind',
    type: 'select',
  }
];

const LibrariesPage = () => {
  // const [response] = useQuery({ query: getResources });
  const response = DummyResponse;

  if (response.fetching) {
    return (<Page themeId="home">
      <Content>
        <div>
          <Table
            options={{ paging: false, padding: 'default' }}
            data={[]}
            columns={columns}
            filters={filters}
          />
        </div>
      </Content>
    </Page>);

  } else if (response.error) {
    if (response.error.message === "[Network] Unauthorized") {
      return <Grid item>
        <Alert severity="error">Unauthorized. Please check your Zoo token in the Settings.</Alert>
      </Grid>;
    }
    return <Grid item>
      <Alert severity="error">{response.error.message}</Alert>
    </Grid>;
  }
  const resources = unwrap<Resource>(response.data.resources);


  const libraryData = generateTableData(resources);

  return (
    <Page themeId="home">
      <Content>
        <div>
          <Table
            options={{ paging: false, padding: 'default' }}
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
