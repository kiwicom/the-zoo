import React from 'react';
import { Content, Page, Table, TableColumn } from '@backstage/core';
import { DummyResponse, Resource, unwrap } from "zoo-api";
import ResourceLink from "../TableComponents/ResourceLink";
import { Chip, Grid } from "@material-ui/core";
import ResourceTypeLabel from "../TableComponents/ResourceTypeLabel";
import Alert from "@material-ui/lab/Alert";


const generateTableData: (resources: Resource[]) => Array<{}> = (resources) => {
  return resources.map(item => {
    return {
      usage: item.usageCount,
      name: item.name,
      version: item.version,
      type: item.type,
    }
  });
};

const columns: TableColumn[] = [
  {
    title: 'Usage',
    field: 'usage',
    type: 'numeric',
    highlight: true,
    render: rowData => <ResourceLink name={rowData.name} id={rowData.id} />
  },
  {
    title: 'Name',
    field: 'name',
    render: rowData => <ResourceLink name={rowData.name} id={rowData.id} />
  },
  {
    title: 'Leatest Version',
    field: 'version',
    render: rowData => <Chip label={rowData.version} />
  },
  {
    title: 'Type',
    field: 'type',
    render: rowData => <ResourceTypeLabel name={rowData.type} />
  }
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
  const resources = unwrap<Resource>(response.data.resources);


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
