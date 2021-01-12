import React from 'react';
import { useQuery, UseQueryState } from 'urql';
import { ErrorPage, Progress } from '@backstage/core';
import Alert from '@material-ui/lab/Alert';


export function useBackend<T>(name: string, query: string, variables: object): [
  T | undefined,
  React.ReactElement | null,
  UseQueryState,
] {
  const [response] = useQuery({ query, variables });
  let obj: T | undefined = undefined;
  let component: React.ReactElement | null = null;


  if (response.fetching) component = <Progress />;
  else if (response.error) {
    component = response.error.message === "[Network] Unauthorized"
      ? <Alert severity="error">Unauthorized. Please check your Zoo token in the Settings.</Alert>
      : <Alert severity="error">{response.error.message}</Alert>
  }
  else if (response.data) {
    if (response.data[name]) obj = response.data[name]
    else component = <ErrorPage status="404" statusMessage="Service not found" />
  }

  return [obj, component, response]
}
