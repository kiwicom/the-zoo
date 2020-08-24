import React, { FC } from 'react';
import {Button, Card, CardContent, Chip, IconButton, Grid, Link, Tooltip, Typography } from '@material-ui/core';
import { Service } from 'zoo-api';
import VibrationIcon from '@material-ui/icons/Vibration';
import AlarmOnIcon from '@material-ui/icons/AlarmOn';
import EventBusyIcon from '@material-ui/icons/EventBusy';
import ReportProblemIcon from '@material-ui/icons/ReportProblem';
import Count from './Count';

type Props = {
  service: Service;
}

const ServicePagerduty: FC<Props> = ({ service }) => (
  <Card>
    <CardContent>

      <Grid container direction="row" justify="space-between">
        <Grid item>
          <Grid container direction="row" justify="flex-start">
            <Grid item><VibrationIcon /></Grid>
            <Grid item>
              <Typography variant="h6">
                <Link href="https://example.pagerduty.com/users/PXXYYZZ">Burt Macklin</Link>
                <Typography component="span"> is On-Call</Typography>
              </Typography>
              <Typography variant="subtitle2" color="textSecondary" paragraph>Team for {service.name}</Typography>
            </Grid>
          </Grid>
        </Grid>
        <Grid item>
          <Grid container direction="row" justify="flex-end">
            <Grid item><Tooltip placement="top" title="Active incidents"><IconButton><Count value={1}><AlarmOnIcon /></Count></IconButton></Tooltip></Grid>
            <Grid item><Tooltip placement="top" title="Incidents during the last week"><IconButton><Count value={2}><EventBusyIcon /></Count></IconButton></Tooltip></Grid>

            <Grid item><Button startIcon={<ReportProblemIcon />} variant="contained" color="secondary">Create incident</Button></Grid>
          </Grid>
        </Grid>
      </Grid>
      <Grid container spacing={1} direction="column">
        <Grid item>
          <Card style={{ borderTop: '2px solid orange' }}>
            <CardContent>
              <Grid container direction="row" justify="space-between">
                <Grid item>
                  <Typography style={{ color: 'orange' }}>
                    <strong>Incident </strong>
                    <Link href="#">[#12345678] Something went quite wrong, but I think you’ll find a great quickfix in no time!</Link>
                  </Typography>
                </Grid>

                <Grid item>
                  <Chip label="status:acknowledged" color="primary" size="small" />
                </Grid>
              </Grid>
              <Typography variant="subtitle2" color="textSecondary">
                {`Task exception was never retrieved future: <Task finished coro=<VirtualPaymentCard.close_later() done, defined at /app/atm/integrations/decorators.py:80> exception=OperationalError('Error 32 while writing to socket. Broken pipe.')>`}
              </Typography>
            </CardContent>
          </Card>
        </Grid>

      </Grid>

    </CardContent>
  </Card >
)
export default ServicePagerduty;
