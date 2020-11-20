import React, { FC } from 'react';
import { useQuery } from 'urql';
import Alert from '@material-ui/lab/Alert';
import { Progress } from '@backstage/core';
import { Button, Card, CardContent, Chip, IconButton, Grid, Link, Tooltip, Typography } from '@material-ui/core';
import { getPagerdutyService, Service, ActiveIncident } from 'zoo-api';
import VibrationIcon from '@material-ui/icons/Vibration';
import AlarmOnIcon from '@material-ui/icons/AlarmOn';
import EventBusyIcon from '@material-ui/icons/EventBusy';
import ReportProblemIcon from '@material-ui/icons/ReportProblem';
import Count from './Count';
import { unwrap } from 'zoo-api/src/client';

type Props = {
  service: Service;
}

const ServicePagerduty: FC<Props> = ({ service }) => {
  if (!service.pagerdutyService) return null;

  const [response] = useQuery({ query: getPagerdutyService, variables: { id: service.id } });

  if (response.fetching) {
    return <Progress />;
  } else if (response.error) {
    return <Alert severity="error">{response.error.message}</Alert>;
  }

  const s: Service = response.data.service;
  const pd = s.pagerdutyInfo;
  if (!pd) return (null);
  const incidents: ActiveIncident[] = unwrap(pd.allActiveIncidents);
  return (
    <Card>
      <CardContent>

        <Grid container direction="row" justify="space-between">
          <Grid item>
            <Grid container direction="row" justify="flex-start">
              <Grid item><VibrationIcon /></Grid>
              <Grid item>
                <Typography variant="h6">
                  <Link href={pd.oncallPerson.htmlUrl}>{pd.oncallPerson.summary}</Link>
                  <Typography component="span"> is On-Call</Typography>
                </Typography>
                <Typography variant="subtitle2" color="textSecondary" paragraph>{pd.summary}</Typography>
              </Grid>
            </Grid>
          </Grid>
          <Grid item>
            <Grid container direction="row" justify="flex-end">
              <Grid item><Tooltip placement="top" title="Active incidents"><IconButton><Count value={pd.allActiveIncidents.totalCount}><AlarmOnIcon /></Count></IconButton></Tooltip></Grid>
              <Grid item><Tooltip placement="top" title="Incidents during the last week"><IconButton><Count value={pd.pastWeekTotal}><EventBusyIcon /></Count></IconButton></Tooltip></Grid>

              <Grid item><Button startIcon={<ReportProblemIcon />} variant="contained" color="secondary" disabled>Create incident</Button></Grid>
            </Grid>
          </Grid>
        </Grid>
        <Grid container spacing={1} direction="column">
          {incidents.map(incident => {
            const color = incident.color === 'yellow' ? "orange" : incident.color;
            return (
              <Grid item key={incident.id}>
                <Card style={{ borderTop: `2px solid ${color}` }}>
                  <CardContent>
                    <Grid container direction="row" justify="space-between">
                      <Grid item>
                        <Typography style={{ color: color }}>
                          <strong>Incident </strong>
                          <Link href={incident.htmlUrl}>{incident.summary}</Link>
                        </Typography>
                      </Grid>

                      <Grid item>
                        <Chip label={`status:${incident.status}`} style={{ backgroundColor: color }} color="secondary" size="small" />
                      </Grid>
                    </Grid>
                    <Typography variant="subtitle2" color="textSecondary">{incident.description}</Typography>
                  </CardContent>
                </Card>
              </Grid>
            )
          })}
        </Grid>

      </CardContent>
    </Card >
  )
}
export default ServicePagerduty;
