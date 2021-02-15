import React from 'react';
import { HeaderTabs } from '@backstage/core';
import { useNavigate, useLocation } from 'react-router-dom';
import { ResourcesTabsLabels } from '../App'

const getTabIndex = (path:string) => {
  const tab = ResourcesTabsLabels.find(x => x.route === path)
  return tab ? tab.id : 0

}

const ResourceTabs = () => {
  const navigate = useNavigate()
  const location = useLocation();

  const doChange = (idx: number): void => {
    const tab = ResourcesTabsLabels.find(x => x.id === idx)
    if (tab) {
      navigate(tab.route)
    }
  }

  return (<HeaderTabs
    selectedIndex={getTabIndex(location.pathname.replace("/resources/", ""))}
    onChange={doChange}
    tabs={ResourcesTabsLabels.map(({ label }, index) => ({
      id: index.toString(),
      label,
    }))}
  />);
};

export default ResourceTabs;
