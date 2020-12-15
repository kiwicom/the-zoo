import React from 'react';
import { Toolbar, Breadcrumbs, Button, Card, CardHeader, Divider, Grid, Link, Typography } from '@material-ui/core';
import { useParams } from 'react-router-dom';
import Alert from '@material-ui/lab/Alert';
import { Progress } from '@backstage/core';
import { useQuery } from 'urql';
import StorageIcon from '@material-ui/icons/Storage';
import DirectionsIcon from '@material-ui/icons/Directions';
import ChatIcon from '@material-ui/icons/Chat'
import HealingIcon from '@material-ui/icons/Healing'
import SchoolIcon from '@material-ui/icons/School';
import SpeedIcon from '@material-ui/icons/Speed'
import SubjectIcon from '@material-ui/icons/Subject';
import LaptopIcon from '@material-ui/icons/Laptop';
import DescriptionIcon from '@material-ui/icons/Description';
import pluralize from 'pluralize';
import ServiceLabel from '../ServiceLabel'
import ServiceRepository from '../ServiceRepository'
import ServiceSentry from '../ServiceSentry'
import ServicePagerduty from '../ServicePagerduty'
import { getService, Service } from 'zoo-api';
import { Link as RouterLink } from 'react-router-dom';

import ContentHeader from '../ContentHeader'

const ServiceDetail = () => {
  const { id } = useParams();
  const [response] = useQuery({ query: getService, variables: { id } });

  if (response.fetching) {
    return <Progress />;
  } else if (response.error) {
    if (response.error.message === "[Network] Unauthorized") {
      return <Alert severity="error">Unauthorized. Please check your Zoo token in the Settings.</Alert>;
    }
    return <Alert severity="error">{response.error.message}</Alert>;
  }

  const service: Service = response.data.service;

  const ViewReport: FC = () => (
    <Button component={RouterLink}
      to={`/services/${service.name}/issues/`}
      state={{service: service}}
      startIcon={<SubjectIcon />}
      variant="contained"
      color="secondary">View report</Button>
  )
  return (
    <>
      <ContentHeader title={service.name}/>
      <Grid container direction="row" justify="space-between">
        <Grid item>
          <Breadcrumbs aria-label="breadcrumb">
            <Link component={RouterLink} color="inherit" to="/services">
              Services
              </Link>
            <Typography color="textPrimary">{service.name}</Typography>
          </Breadcrumbs>
        </Grid>

        <Grid item>
          <ServiceLabel name="status" value={service.status} />
          <ServiceLabel name="impact" value={service.impact} />
        </Grid>
      </Grid>

      <Grid container direction="column">
        <Grid item>

          <Card>
            <Toolbar>
              <Button>Overview</Button>
              <Button startIcon={<DirectionsIcon />}>API</Button>
              <Button startIcon={<StorageIcon />}>Infrastructure</Button>

              <Divider orientation="vertical" style={{ flexGrow: 1 }} />

              <Button startIcon={<ChatIcon />}>Discussion</Button>
              <Button startIcon={<SpeedIcon />}>Dashboard</Button>
              <Button startIcon={<DescriptionIcon />}>Logs</Button>
              <Button startIcon={<SchoolIcon />}>Docs</Button>
              <Button startIcon={<LaptopIcon />}>env:default</Button>
            </Toolbar>
          </Card>
        </Grid>

        <Grid item>
          <ServicePagerduty service={service} />
        </Grid>

        <Grid item>
          <Card>
            <CardHeader
              avatar={<HealingIcon />}
              title={<Typography variant="h6">Auditing report</Typography>}
              subheader={`${pluralize("issue", service.repository.issues.length, true)} found during the last analysis`}
              action={<ViewReport />}
              style={{ paddingBottom: '16px' }} />
          </Card>
        </Grid>

        <Grid item>
          <ServiceRepository repository={service.repository} />
        </Grid>

        <Grid item>
          <ServiceSentry service={service} />
        </Grid>

      </Grid>
    </>
  )
};

export default ServiceDetail;
