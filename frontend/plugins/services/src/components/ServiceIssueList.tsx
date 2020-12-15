import React from 'react';
import { Link as RouterLink, useParams } from 'react-router-dom';
import { Typography, Grid, Breadcrumbs, Link, } from '@material-ui/core'
import Alert from '@material-ui/lab/Alert';
import { Progress } from '@backstage/core';
import { useQuery } from 'urql';
import { getService, Service } from 'zoo-api';
import ContentHeader from './ContentHeader'


const ServiceIssueCategory = ({ service }: {service: Service}) => {
  return (
    <>
    {service.repository.issues.map(issue => (
      <dl>
        <dt style={{ display: 'inline-block' }}>Kind Key</dt>
        <dl><strong>{issue.kindKey}</strong></dl>
        <dt style={{ display: 'inline-block' }}>Status</dt>
        <dl><strong>{issue.status}</strong></dl>
        <dt style={{ display: 'inline-block' }}>Remote Issue Id</dt>
        <dl><strong>{issue.remoteIssueId}</strong></dl>
        <dt style={{ display: 'inline-block' }}>Comment</dt>
        <dl><strong>{issue.comment}</strong></dl>
        <dt style={{ display: 'inline-block' }}>Last Check</dt>
        <dl><strong>{issue.lastCheck}</strong></dl>
      </dl>
    ))}
    </>
  )
}
const ServiceIssueList = () => {
  const { name } = useParams();
  const [response] = useQuery({ query: getService, variables: { name } });

  if (response.fetching) {
    return <Progress />;
  } else if (response.error) {
    if (response.error.message === "[Network] Unauthorized") {
      return <Alert severity="error">Unauthorized. Please check your Zoo token in the Settings.</Alert>;
    }
    return <Alert severity="error">{response.error.message}</Alert>;
  }
  const service: Service = response.data.service;

  return (
    <>
      <ContentHeader title={`Audit results for ${service.name}`} />
      <Grid container direction="row" justify="space-between">
        <Grid item>
          <Breadcrumbs aria-label="breadcrumb">
            <Link component={RouterLink} color="inherit" to="/services">
              Services
              </Link>
            <Typography color="textPrimary">{service.name}</Typography>
          </Breadcrumbs>
        </Grid>
      </Grid>
      <ServiceIssueCategory service={service}/>
    </>
  )
};

export default ServiceIssueList;
