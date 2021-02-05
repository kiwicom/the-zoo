import React from "react";
import {Chip} from "@material-ui/core";

interface Props {
  name: string
}
interface colorInfo {
  backgroundColor: string;
}

interface MappingDict {
  [key: string]: colorInfo;
}
const choiceColors: MappingDict = {
  'Language': {backgroundColor:'brown'},
  'Operating System': {backgroundColor:'gray'},
  'Javascript Library': {backgroundColor:'gold'},
  'Python Library': {backgroundColor:'green'},
  'Go Library': {backgroundColor:'teal'},
  'Rust Library': {backgroundColor:'orange'},
  'Erlang Library': {backgroundColor:'red'},
  'Docker Image': {backgroundColor:'blue'},
  'Gitlab-ci.yml': {backgroundColor:'lightsalmon'},
}


const ResourceTypeLabel = ({ name }: Props) => {
  const backgroundColor = choiceColors[name]
  const label = name.includes("Library") ? name.substring(0, name.indexOf(" Library")) : name;

  return (
    <Chip label={label} style={backgroundColor} color='primary' />
  )
};

export default ResourceTypeLabel;
