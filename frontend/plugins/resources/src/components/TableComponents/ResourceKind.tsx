import React from "react";
import { Chip } from "@material-ui/core";

interface Props {
  name: string
}

const ResourceKind = ({ name }: Props) => {
  let value = "Public"
  let backgroundColor = {backgroundColor:'gray'}

  if (name.includes("kiwi-")) {
    value = "Internal"
    backgroundColor = {backgroundColor:'#795548'}
  }

  return (
    <Chip label={value} style={backgroundColor} color='primary' />
  )
};

export default ResourceKind;
