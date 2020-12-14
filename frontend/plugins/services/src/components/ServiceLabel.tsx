import React from 'react';
import { Chip } from '@material-ui/core';

interface MappingDict {
  [key: string]: string;
}

const choiceColors: MappingDict = {
  // We might want to get this enum from the backend
  'beta': 'DarkOrange',
  'production': 'ForestGreen',
  'deprecated': 'Crimson',
  'discontinuated': 'DimGray',

  'profit': 'Black',
  'customers': 'FireBrick',
  'employees': 'RoyalBlue',
}

interface Props {
  name: string
  value: string
}

const ServiceLabel = ({ name, value }: Props) => {
  if (!value || value === "undefined") return null;
  const choice = value.toLowerCase(); // Should be fixed in backend instead

  const color = choiceColors[choice] || "Gray";

  return <Chip label={`${name}:${choice}`} style={{ color: "white", backgroundColor: color }} size="small" />
}


export default ServiceLabel;
