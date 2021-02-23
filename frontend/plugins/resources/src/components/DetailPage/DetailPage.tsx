import React from 'react';
import DetailPageHeader from './DetailPageHeader';
import ResourcesHeader from '../ResourcesHeader';
import Grid from '@material-ui/core/Grid';
import VersionDistribution from './VersionDistribution';
import VersionList from './VersionList';
import { Outlet, useParams } from 'react-router-dom';
import { Content, Page } from '@backstage/core';
import { Card, CardContent } from '@material-ui/core';
import { Dependency, DependencyUsage, getDependency, unwrap, useBackend } from 'zoo-api';
import { sortDependencyUsages, SortedVersions } from './VersionList';

export interface ChartDataInterface {
  name: string;
  value: number;
}


const Detailpage = () => {
  const params = useParams();

  const generateChartData = (resources: SortedVersions) => Object.keys(resources).map((resource) => ({
    name: resource,
    value: resources[resource].length
  }));

  const getChartColors = (chartData:ChartDataInterface[]) => {
    function randomHSL(){
      return `hsla(${~~(360 * Math.random())},70%,70%,0.8)`
    }

    return Array.from({length: chartData.length}, () => randomHSL())
  }

  const [response, component] = useBackend<Dependency>("dependency", getDependency, params);

  if (component) return <Grid item>{component}</Grid>;
  if (!response) return null;

  const versions = unwrap<DependencyUsage>(response.dependencyUsages);
  const chartData = generateChartData(sortDependencyUsages(versions));

  return (
    <>
      <ResourcesHeader title="Kiwi.com resources" description="Libraries, Languages, CI templates" />
      <Page themeId="home">
        <Content>
          <DetailPageHeader resource={response} />
            <Outlet />
          <Card>
            <CardContent>
              <Grid container spacing={3}>
                <Grid container item xs={6} alignItems="center" justify="center">
                  <VersionDistribution chartData={chartData} chartColors={getChartColors(chartData)} />
                </Grid>
                <Grid item xs={6}>
                  <VersionList activeVersions={versions} dependencyId={response.id} />
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
