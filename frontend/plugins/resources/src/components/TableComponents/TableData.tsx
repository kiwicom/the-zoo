import {Dependency} from 'zoo-api';
import {TableColumn} from '@backstage/core';
import ResourceLink from './ResourceLink';
import {Chip} from '@material-ui/core';
import ResourceTypeLabel from './ResourceTypeLabel';
import React from 'react';


export const commonColumns: TableColumn[] = [
  {
    title: 'Usage',
    field: 'usage',
    type: 'numeric',
    highlight: true,
  },
  {
    title: 'Name',
    field: 'name',
    render: (rowData:object) => <ResourceLink name={rowData.name} id={rowData.id} />
  },
  {
    title: 'Leatest Version',
    field: 'version',
    render: (rowData:object) => <Chip label={rowData.version} />
  },
  {
    title: 'Type',
    field: 'type',
    render: (rowData:object) => <ResourceTypeLabel name={rowData.type} />
  },
];

export const capitalize: (word:string) =>string = (word) => {
  const cleanWord = word.replace('_LIBRARY','').split('_').join(' ').toLowerCase()
  return cleanWord[0].toUpperCase() + cleanWord.slice(1)
}

export const generateTableData: (resources: Dependency[]) => Array<{}> = (resources) => {
  return resources.map(item => {
    return {
      id: item.id,
      usage: item.dependencyUsages.edges.length,
      name: item.name,
      version: item.dependencyVersion,
      type: capitalize(item.type),
      kind: item.name,
    }
  });
};
