import { Box } from '@material-ui/core';
import React from 'react';
import { useParams, useSearchParams } from 'react-router-dom';
import SwaggerUI from "swagger-ui-react";
import "swagger-ui-react/swagger-ui.css";
import { useQuery } from 'urql';
import { Environment, getService, Service, unwrap } from 'zoo-api';

const ServiceApiDoc = () => {
  const { id } = useParams();
  const [searchParams] = useSearchParams();
  const [response] = useQuery({ query: getService, variables: { id } });
  const service: Service = response.data.service;

  if (!service) return null;

  const environment = unwrap<Environment>(service.environments).find(
    env => env.name === searchParams.get("environment")
  );

  if (!environment) return null

  return (
    <Box bgcolor="rgba(255, 255, 255, 0.9)">
      <SwaggerUI url={environment.openApiUrl} />
    </Box>
  )
};

export default ServiceApiDoc;
