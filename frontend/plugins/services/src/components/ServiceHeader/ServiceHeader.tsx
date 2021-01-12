import { Breadcrumbs, Button, Card, Divider, Grid, Link, Toolbar, Typography, Menu, MenuItem } from '@material-ui/core';
import ChatIcon from '@material-ui/icons/Chat';
import DescriptionIcon from '@material-ui/icons/Description';
import DirectionsIcon from '@material-ui/icons/Directions';
import SchoolIcon from '@material-ui/icons/School';
import SpeedIcon from '@material-ui/icons/Speed';
import StorageIcon from '@material-ui/icons/Storage';
import React, { ReactNode, MouseEvent, useState } from 'react';
import { Link as RouterLink, useSearchParams, useLocation, useNavigate } from 'react-router-dom';
import { Environment, Service, unwrap } from 'zoo-api';
import ServiceLabel from '../ServiceLabel';
import { makeStyles } from '@material-ui/core/styles';

const urls = (s: Service) => {
  return {
    overview: `/services/${s.id}/${s.name}/`,
    openapi: `/services/${s.id}/${s.name}/swagger-ui/`
  }
}

const useStyles = makeStyles({
  root: {
    textTransform: "uppercase"
  }
});

const ServiceHeader = ({ children, service }: { children: ReactNode, service: Service }) => {
  const [qs] = useSearchParams();
  const environments = unwrap<Environment>(service.environments);
  const env = environments.find(env => env.name === qs.get("environment"));
  const [environment, setEnvironment] = useState<Environment | undefined>(env);
  const [anchorEl, setAnchorEl] = React.useState<null | HTMLElement>(null);
  const classes = useStyles();

  const location = useLocation();
  const navigate = useNavigate();

  const selectEnvironment = (event: MouseEvent<HTMLButtonElement>) => {
    setAnchorEl(event.currentTarget);
  };
  const handleClose = () => {
    setAnchorEl(null);
  };
  const setEnv = (env: Environment) => {
    handleClose();
    setEnvironment(env);

    // Hack: https://github.com/ReactTraining/react-router/issues/7353
    // Replacement for: setSearchParams({"environment": env.name})
    qs.set("environment", env.name)
    navigate({ pathname: location.pathname, search: `?${qs.toString()}` });
  }

  return (
    <>
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

          <Button disabled={!environment} aria-controls="env-menu" aria-haspopup="true" onClick={selectEnvironment}>
            {environment ? environment.name : "No Environment"}
          </Button>
          {environment ?
            <Menu id="env-menu" anchorEl={anchorEl} keepMounted open={Boolean(anchorEl)} onClose={handleClose}>
              {
                unwrap<Environment>(service.environments).map(env => (
                  <MenuItem classes={classes} key={env.name} disabled={env.name === environment.name} onClick={() => setEnv(env)}>
                    {env.name}
                  </MenuItem>)
                )
              }
            </Menu>
            : null
          }
        </Grid>
      </Grid>

      <Grid container direction="column">
        <Grid item>

          <Card>
            <Toolbar>
              <Button component={RouterLink}
                to={`${urls(service).overview}?${qs.toString()}`}
                state={{ service }}
              >Overview</Button>
              <Button component={RouterLink}
                to={`${urls(service).openapi}?${qs.toString()}`}
                state={{ service }}
                startIcon={<DirectionsIcon />}
              >API</Button>
              <Button disabled startIcon={<StorageIcon />}>Infra</Button>

              <Divider orientation="vertical" style={{ flexGrow: 1 }} />

              <Button disabled startIcon={<ChatIcon />}>Discussion</Button>
              <Button disabled startIcon={<SpeedIcon />}>Dashboard</Button>
              <Button disabled startIcon={<DescriptionIcon />}>Logs</Button>
              <Button disabled startIcon={<SchoolIcon />}>Docs</Button>
            </Toolbar>
          </Card>
        </Grid>

        {children}

      </Grid>
    </>
  )
};

export default ServiceHeader;
