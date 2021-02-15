
import React from 'react';
import { Outlet, useParams, useSearchParams } from 'react-router-dom';
import { Environment, unwrap, useBackend, getService, Service } from 'zoo-api';
import ServiceHeader from '../ServiceHeader';

import ContentHeader from '../ContentHeader';

const ServiceDetail = () => {
  const params = useParams();
  const [qs, setQueryString] = useSearchParams();
  const [service, component] = useBackend<Service>("service", getService, params);

  if (component) return (<><ContentHeader title={params.name} />{component}</>);
  if (!service) return null;

  const environments = unwrap<Environment>(service.environments);
  if (environments.length && !qs.get("environment")) {
    setQueryString({ environment: environments[0].name });
  };

  return (
    <>
      <ContentHeader title={service.name} />
      <ServiceHeader service={service}>
        <Outlet />
      </ServiceHeader>
    </>
  )
};

export default ServiceDetail;
