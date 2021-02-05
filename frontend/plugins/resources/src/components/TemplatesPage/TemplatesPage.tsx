import React from 'react';
import {Content, Page, Table, TableColumn} from '@backstage/core';
import {DummyResponse, Edge, Resource} from "../../../../../packages/zoo-api";
import ResourceLink from "../TableComponents/ResourceLink";
import {Chip, Grid} from "@material-ui/core";
import ResourceTypeLabel from "../TableComponents/ResourceTypeLabel";
import ResourceKind from "../TableComponents/ResourceKind";
import Alert from "@material-ui/lab/Alert";


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

const TemplatesPage = () => {
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

  const templateData = generateTableData(resources);

  return (
    <Page themeId="home">
      <Content>
        <div>
          <Table
            options={{ paging: true, padding: 'default' }}
            data={templateData}
            columns={columns}
          />
        </div>
      </Content>
    </Page>
  )
};

export default TemplatesPage;
