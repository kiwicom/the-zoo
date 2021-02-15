import React from 'react';
import { ContentHeader as BackstageContentHeader, SupportButton } from '@backstage/core';
import {Breadcrumbs, Button, Chip, Grid, Link, Typography} from "@material-ui/core";
import {Link as RouterLink} from "react-router-dom";
import ResourceTypeLabel from "../TableComponents/ResourceTypeLabel";

interface Props {
  resource?: any // change to type resource
}

const DetailPageHeader = ({ resource }: Props) => {
  return (
    <>
      <BackstageContentHeader title={resource.name} description={resource.description}>
        <SupportButton slackChannel="#plz-platform-software">A description of your plugin goes here.</SupportButton>
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
          <ResourceTypeLabel name={resource.type} />
        </Grid>
      </Grid>
    </>
  )
};

export default DetailPageHeader;
