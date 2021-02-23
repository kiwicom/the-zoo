import React from 'react';
import ResourceTypeLabel from '../TableComponents/ResourceTypeLabel';
import { ContentHeader as BackstageContentHeader, SupportButton } from '@backstage/core';
import { Breadcrumbs, Grid, Link, Typography } from '@material-ui/core';
import { Link as RouterLink } from 'react-router-dom';
import { capitalize } from '../TableComponents/TableData';
import { Dependency } from 'zoo-api';

interface Props {
  resource: Dependency
}

const DetailPageHeader = ({ resource }: Props) => {

  return (
    <>
      <BackstageContentHeader title={resource.name} description="">
        <SupportButton slackChannel="#plz-platform-software"></SupportButton>
      </BackstageContentHeader>
      <Grid container direction="row" justify="space-between">
        <Grid item>
          <Breadcrumbs aria-label="breadcrumb">
            <Link component={RouterLink} color="inherit" to="/resources">
              Resources
            </Link>
            <Typography color="textPrimary">{resource.name}</Typography>
          </Breadcrumbs>
        </Grid>

        <Grid item>
          <ResourceTypeLabel name={capitalize(resource.type)} />
        </Grid>
      </Grid>
    </>
  )
};

export default DetailPageHeader;
