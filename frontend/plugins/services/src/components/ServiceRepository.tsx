import React, { FC } from 'react';
import { Breadcrumbs, Button, IconButton, Card, CardContent, Grid, Link, Tooltip, Typography } from '@material-ui/core';

import BugReportIcon from '@material-ui/icons/BugReport';
import CallSplitIcon from '@material-ui/icons/CallSplit';
import CodeIcon from '@material-ui/icons/Code';
import FilterNoneIcon from '@material-ui/icons/FilterNone';
import PagesIcon from '@material-ui/icons/Pages';
import PersonIcon from '@material-ui/icons/Person';
import StarIcon from '@material-ui/icons/Star';

import Count from './Count'
import { Repository } from 'zoo-api';


type Props = {
  repository: Repository;
}

const ServiceRepository: FC<Props> = ({ repository }) => (
  <Card>
    <CardContent>
      <Grid container direction="row" justify="space-between">

        <Grid item>
          <Grid container direction="row" >
            <Grid item style={{paddingTop: '12px'}}><PagesIcon /></Grid>
            <Grid item>
              <Breadcrumbs>
                <Link href={repository.url.slice(0, repository.url.lastIndexOf('/'))} target="_blank" rel="noopener">
                  <Typography variant="h6" color="textPrimary">{repository.owner}</Typography>
                </Link>
                <Link href={repository.url} target="_blank" rel="noopener">
                  <Typography variant="h6">{repository.name}</Typography>
                </Link>
              </Breadcrumbs>
            </Grid>
          </Grid>
        </Grid>

        <Grid item>
          <Grid container direction="row" justify="flex-end">
            <Grid item><Tooltip placement="top" title="Stars"><IconButton><Count value={3}><StarIcon /></Count></IconButton></Tooltip></Grid>
            <Grid item><Tooltip placement="top" title="Forks"><IconButton><Count value={1}><FilterNoneIcon /></Count></IconButton></Tooltip></Grid>
            <Grid item><Tooltip placement="top" title="Branches"><IconButton><Count value={1}><CallSplitIcon /></Count></IconButton></Tooltip></Grid>
            <Grid item><Tooltip placement="top" title="Issues"><IconButton><Count value={1}><BugReportIcon /></Count></IconButton></Tooltip></Grid>
            <Grid item><Tooltip placement="top" title="Members"><IconButton><Count value={6}><PersonIcon /></Count></IconButton></Tooltip></Grid>

            <Grid item><Button startIcon={<CodeIcon />} variant="contained" color="secondary">Open issue</Button></Grid>
          </Grid>
        </Grid>

      </Grid>
    </CardContent>
  </Card>
)

export default ServiceRepository;
