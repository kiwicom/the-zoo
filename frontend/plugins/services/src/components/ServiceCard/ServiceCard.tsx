import React from 'react';
import { Link, IconButton, Tooltip, Grid, Card, CardContent, Typography } from '@material-ui/core';
import ChatBubbleIcon from '@material-ui/icons/ChatBubble';
import BarChartIcon from '@material-ui/icons/BarChart';
import CodeIcon from '@material-ui/icons/Code';
import SchoolIcon from '@material-ui/icons/School';
import PriorityHighIcon from '@material-ui/icons/PriorityHigh';
import { Link as RouterLink } from 'react-router-dom';

import { Service } from 'zoo-api';
import ServiceLabel from '../ServiceLabel'

interface ActionProps {
  title: string
  label: string
  url: (string | null)
  icon: React.FC
}

const ServiceAction = ({ title, label, url, icon: Icon }: ActionProps) => {
  const ActiveAction = ({ href }: { href: string }) => (
    <Link href={href} target="_blank" rel="noopener">
      <IconButton aria-label={label}>
        <Icon />
      </IconButton>
    </Link>
  )

  return (
    <Tooltip placement="top" title={title}>
      <span>
        {url
          ? <ActiveAction href={url} />
          : <IconButton disabled aria-label={label}> <Icon /> </IconButton>
        }
      </span>
    </Tooltip>
  )
}


const ServiceCard = ({ service }: { service: Service }) => (
  <Card>
    <CardContent>
      <Grid container direction="row" justify="space-between" alignItems="center">

        <Grid item>
          <Grid container alignItems="baseline">
            <Grid item>
              <Typography variant="h5">
                <Link component={RouterLink} to={`/services/${service.id}/${service.name}`}>{service.name}</Link>
              </Typography>
            </Grid>
            <Grid item>
              owned by&nbsp;
              <Link href={service.repository.url} target="_blank" rel="noopener">
                {service.owner}
              </Link>
            </Grid>
          </Grid>
          <ServiceLabel name="status" value={service.status} />
          <ServiceLabel name="impact" value={service.impact} />
        </Grid>

        <Grid item>
          <ServiceAction title="Help" label="help" url={service.slackChannel ? `https://skypicker.slack.com/messages/${service.slackChannel}` : null} icon={ChatBubbleIcon} />
          <ServiceAction title="Repository" label="repository" url={service.repository.url} icon={CodeIcon} />
          <ServiceAction title="Dashboard" label="dashboard" url={null} icon={BarChartIcon} />
          <ServiceAction title="Alerts" label="alerts" url={null} icon={PriorityHighIcon} />
          <ServiceAction title="Docs" label="docs" url={service.docsUrl} icon={SchoolIcon} />
        </Grid>

      </Grid>
    </CardContent>
  </Card>
)

export default ServiceCard;
