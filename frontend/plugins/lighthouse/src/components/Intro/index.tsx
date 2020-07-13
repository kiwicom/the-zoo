/*
 * Copyright 2020 Spotify AB
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
import React, { useState } from 'react';
import { useLocalStorage } from 'react-use';
import Markdown from 'react-markdown';
import { ContentHeader, InfoCard } from '@backstage/core';
import { makeStyles, Button, Grid, Tabs, Tab } from '@material-ui/core';
import CloseIcon from '@material-ui/icons/Close';

import LighthouseSupportButton from '../SupportButton';

export const LIGHTHOUSE_INTRO_LOCAL_STORAGE =
  '@backstage/lighthouse-plugin/intro-dismissed';

const USE_CASES = `
Google's [Lighthouse](https://developers.google.com/web/tools/lighthouse) auditing tool for websites
is a great open-source resource forbenchmarking and improving the accessibility, performance, SEO, and best practices of your site.
At Spotify, we keep track of Lighthouse audit scores over time to look at trends and overall areas for investment.

This plugin allows you to generate on-demand Lighthouse audits for websites, and to track the trends for the
top-level categories of Lighthouse at a glance.

In the future, we hope to add support for scheduling audits (which we do internally), as well as allowing
custom runs of Lighthouse to be ingested (for auditing sites that require authentication or some session state).
`;

const SETUP = `
To get started, you will need a running instance of [lighthouse-audit-service](https://github.com/spotify/lighthouse-audit-service).
_It's likely you will need to enable CORS when running lighthouse-audit-service. Initialize the app
with the environment variable \`LAS_CORS\` set to \`true\`._

When you have an instance running that Backstage can hook into, make sure to export the plugin in
your app's [\`plugins.ts\`](https://github.com/spotify/backstage/blob/master/packages/app/src/plugins.ts)
to enable the plugin:

\`\`\`js
import { default as LighthousePlugin } from '@backstage/plugin-lighthouse';
export LighthousePlugin;
\`\`\`

Then, you need to use the \`lighthouseApiRef\` exported from the plugin to initialize the Rest API in
your [\`apis.ts\`](https://github.com/spotify/backstage/blob/master/packages/app/src/apis.ts).

\`\`\`js
import { ApiHolder, ApiRegistry } from '@backstage/core';
import {
  lighthouseApiRef,
  LighthouseRestApi,
} from '@backstage/plugin-lighthouse';

const builder = ApiRegistry.builder();

export const lighthouseApi =
  new LighthouseRestApi(/* your service url here! */);
builder.add(lighthouseApiRef, lighthouseApi);

export default builder.build() as ApiHolder;
\`\`\`
`;

const useStyles = makeStyles((theme) => ({
  tabs: { marginBottom: -18 },
  tab: { minWidth: 72, paddingLeft: 1, paddingRight: 1 },
  content: { marginBottom: theme.spacing(2) },
  closeButtonContainer: { height: '100%' },
  closeButtonItem: { paddingBottom: 0 },
}));

function GettingStartedCard() {
  const classes = useStyles();
  const [value, setValue] = useState(0);
  return (
    <InfoCard
      title="Get started"
      subheader={
        <Tabs
          value={value}
          indicatorColor="primary"
          textColor="primary"
          onChange={(_ev, newValue: number) => setValue(newValue)}
          aria-label="get started tabs"
          className={classes.tabs}
        >
          <Tab className={classes.tab} label="Use cases" />
          <Tab className={classes.tab} label="Setup" />
        </Tabs>
      }
      divider
      actions={
        <>
          <Grid container direction="row" justify="flex-end">
            <Grid item>
              <Button
                component="a"
                href="https://github.com/spotify/lighthouse-audit-service"
                size="small"
                target="_blank"
              >
                Check out the README
              </Button>
            </Grid>
          </Grid>
        </>
      }
    >
      {value === 0 && <Markdown source={USE_CASES} />}
      {value === 1 && <Markdown source={SETUP} />}
    </InfoCard>
  );
}

export interface Props {
  onDismiss?: () => void;
}

export default function LighthouseIntro({ onDismiss = () => {} }: Props) {
  const classes = useStyles();
  const [dismissed, setDismissed] = useLocalStorage(
    LIGHTHOUSE_INTRO_LOCAL_STORAGE,
    false,
  );

  if (dismissed) return null;

  return (
    <>
      <ContentHeader title="Welcome to Lighthouse in Backstage!">
        <LighthouseSupportButton />
      </ContentHeader>
      <Grid className={classes.content} container spacing={3} direction="row">
        <Grid item xs={12} sm={6} md={4}>
          <GettingStartedCard />
        </Grid>
        {/* TODO add link and image for blog post here */}
        {/* <Grid item xs={12} sm={6} md={4}>
          <InfoCard>Blog</InfoCard>
        </Grid> */}
        <Grid item xs={12} sm={6} md={8}>
          <Grid
            container
            justify="flex-end"
            alignItems="flex-end"
            className={classes.closeButtonContainer}
          >
            <Grid item className={classes.closeButtonItem}>
              <Button
                variant="text"
                onClick={() => {
                  onDismiss();
                  setDismissed(true);
                }}
              >
                <CloseIcon /> Hide intro
              </Button>
            </Grid>
          </Grid>
        </Grid>
      </Grid>
    </>
  );
}
