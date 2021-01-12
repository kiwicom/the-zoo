import { Button, Card, CardHeader, Grid, Typography } from '@material-ui/core';
import HealingIcon from '@material-ui/icons/Healing';
import SubjectIcon from '@material-ui/icons/Subject';
import pluralize from 'pluralize';
import React from 'react';
import { useSearchParams, Link as RouterLink, useParams } from 'react-router-dom';
import { getService, Service, useBackend } from 'zoo-api';
import ServicePagerduty from '../ServicePagerduty';
import ServiceRepository from '../ServiceRepository';
import ServiceSentry from '../ServiceSentry';


const ServiceOverview = () => {
  const [service, component] = useBackend<Service>("service", getService, useParams());
  const [qs] = useSearchParams();

  if (component) return component;
  if (!service) return null;

  const ViewReport: React.FC = () => (
    <Button component={RouterLink}
      to={`/services/${service.id}/${service.name}/issues/?${qs.toString()}`}
      state={{ service }}
      startIcon={<SubjectIcon />}
      variant="contained"
      color="secondary"
    >View report</Button>
  )

  return (
    <>
      <Grid item>
        <ServicePagerduty service={service} />
      </Grid>

      <Grid item>
        <Card>
          <CardHeader
            avatar={<HealingIcon />}
            title={<Typography variant="h6">Auditing report</Typography>}
            subheader={`${pluralize("issue", service.repository.issues.edges.length, true)} found during the last analysis`}
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
    </>
  )
};

export default ServiceOverview;
