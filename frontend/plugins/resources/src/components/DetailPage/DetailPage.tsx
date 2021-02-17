import React from 'react';
import {Outlet, useParams} from "react-router-dom";
import DetailPageHeader from "./DetailPageHeader";
import ResourcesHeader from "../ResourcesHeader";
import {Content, Page, Table} from "@backstage/core";
import {Card, CardContent, LinearProgress} from "@material-ui/core";

import Grid from '@material-ui/core/Grid';
import VersionDistribution from "./VersionDistribution";
import VersionList from "./VersionList";
import {DummyResourceResponse} from "zoo-api";
import Alert from "@material-ui/lab/Alert";


const Detailpage = () => {
  const params = useParams();
  const resourceId = params.id;

  const generateChartData = (resources) => resources.map(resource => ({
    name: resource.version,
    value: resource.versionList.edges.length
  }));

  const getChartColors = (chartData) => {
    function randomHSL(){
      return `hsla(${~~(360 * Math.random())},70%,70%,0.8)`
    }

    return Array.from({length: chartData.length}, () => randomHSL())
  }


  // const [response] = useQuery({ query: getResource });
  const response = DummyResourceResponse;
  if (response.fetching) {
    return (<Page themeId="home">
      <Content>
        <div>
          <LinearProgress />
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
  const resource = response.data.resource
  const chartData = generateChartData([resource])
  return (
    <>
      <ResourcesHeader title="Kiwi.com resources" description="Libraries, Languages, CI templates" />
      <Page themeId="home">
        <Content>
          <DetailPageHeader resource={resource} />
            <Outlet />
          <Card>
            <CardContent>
              <Grid container spacing={3}>
                <Grid container item xs={6} alignItems="center" justify="center">
                  <VersionDistribution chartData={chartData} chartColors={getChartColors(chartData)} />
                </Grid>
                <Grid item xs={6}>
                  <VersionList versionList={[resource]} />
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Content>
      </Page>
    </>
  )
};

export default Detailpage;
