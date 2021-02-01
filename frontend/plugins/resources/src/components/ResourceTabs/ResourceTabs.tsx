import React from 'react';
import { HeaderTabs } from '@backstage/core';
import { useNavigate } from 'react-router-dom';
import { ResourcesTabsLabels } from '../App'

const ResourceTabs = () => {
  const navigate = useNavigate()

  const doChange = (idx: number): void => {
    const tab = ResourcesTabsLabels.find(x => x.id === idx)
    if (tab) {
      navigate(tab.route)
    }
  }

  return (<HeaderTabs
    onChange={doChange}
    tabs={ResourcesTabsLabels.map(({ label }, index) => ({
      id: index.toString(),
      label,
    }))}
  />);
};

export default ResourceTabs;
