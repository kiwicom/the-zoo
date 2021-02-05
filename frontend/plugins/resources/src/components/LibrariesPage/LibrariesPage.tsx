import React from 'react';
import { Content, Page, Table, TableColumn, TableFilter} from '@backstage/core';
import { getResources, DummyResponse, Resource, Edge } from 'zoo-api';
// import {useQuery} from "urql";
import {Chip, Grid} from "@material-ui/core";
import Alert from '@material-ui/lab/Alert';

import ResourceKind from "../TableComponents/ResourceKind";
import ResourceTypeLabel from "../TableComponents/ResourceTypeLabel";
import ResourceLink from "../TableComponents/ResourceLink";


const generateTableData: (resources: Array<Resource>) => Array<{}> = (resources) => {
  const data: Array<{}> = [];
  for(let i=0; i<resources.length; i++){
    data.push({
      usage: resources[i].usageCount,
      name: <ResourceLink name={resources[i].name} id={resources[i].id} />,
      version: <Chip label={resources[i].version} />,
      type: <ResourceTypeLabel name={resources[i].type} />,
      kind: <ResourceKind name={resources[i].name} />,
    });
  }

  return data;
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
  },
  {
    title: 'Leatest Version',
    field: 'version',
  },
  {
    title: 'Type',
    field: 'type',
  },
  {
    title: 'Kind',
    field: 'kind',
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
  const resources: Resource[] = response.data.resources.edges.map((edge: Edge) => edge.node);

  const libraryData = generateTableData(resources);

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
