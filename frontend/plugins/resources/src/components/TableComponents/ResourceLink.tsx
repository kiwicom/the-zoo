import React from "react";
import { Link as RouterLink } from "react-router-dom";
import { Link } from '@material-ui/core';

interface Props {
  name: string,
  id: string
}

const ResourceLink = ({ name, id}: Props) => {
  return (
    <Link component={RouterLink} to={`/resources/${id}/${name}`}>{name}</Link>
  );
};

export default ResourceLink;
