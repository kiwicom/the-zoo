import React from "react";
import {Header, HeaderLabel} from "@backstage/core";

interface Props {
  title?: string
  description?: string
}

const ResourcesHeader = ({ title, description }: Props) => {

  return (
    <Header title={title} subtitle={description}>
      <HeaderLabel label="Owner" value="Platform Software Squad" />
      <HeaderLabel label="Lifecycle" value="Alpha" />
    </Header>
  )
};

export default ResourcesHeader;
