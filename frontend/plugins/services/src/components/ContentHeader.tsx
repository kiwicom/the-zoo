import React from 'react';
import { Button } from '@material-ui/core';
import SettingsIcon from '@material-ui/icons/Settings';
import { ContentHeader as BackstageContentHeader, SupportButton } from '@backstage/core';
import { useSettings } from '../state';

interface Props {
  title?: string
  description?: string
}

const ContentHeader = ({ title, description }: Props) => {
  const [, { showSettings }] = useSettings();

  return (
    <BackstageContentHeader title={title} description={description}>
      <Button onClick={() => showSettings()} startIcon={<SettingsIcon />}>Settings</Button>
      <SupportButton slackChannel="#plz-platform-software">A description of your plugin goes here.</SupportButton>
    </BackstageContentHeader>
  )
};

export default ContentHeader;
