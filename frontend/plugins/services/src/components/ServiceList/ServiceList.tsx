
import React, { FC } from 'react';
import { Grid } from '@material-ui/core';
import { Skeleton } from '@material-ui/lab';
import Alert from '@material-ui/lab/Alert';
import { useQuery } from 'urql';
import { getServices, Service, Edge } from 'zoo-api';
import ServiceCard from '../ServiceCard';

const ServiceList: FC<{}> = () => {
  const [response] = useQuery({ query: getServices });

  if (response.fetching) {
    return (
      <Grid container spacing={1} direction="column">
        {Array.from({ length: 10 }, (_, idx) => (
          <Skeleton variant="rect" animation="wave" width="100%" height={105} style={{ marginBottom: '8px' }} key={idx} />
        ))}
      </Grid>
    );
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

  const services: Service[] = response.data.services.edges.map((edge: Edge) => edge.node);

  return (
    <Grid container spacing={1} direction="column">
      {services.map(service => (
        <Grid item key={service.id}>
          <ServiceCard service={service} key={service.id} />
        </Grid>
      ))}
    </Grid>
  )
};

export default ServiceList;
