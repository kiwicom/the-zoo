import React, { FC } from 'react'
import { Typography, Grid } from '@material-ui/core'
import {
  InfoCard,
  Header,
  Page,
  pageTheme,
  Content,
  ContentHeader,
  HeaderLabel,
  SupportButton,
} from '@backstage/core'
import ExampleFetchComponent from '../ExampleFetchComponent'
import ServiceCard from '../ServiceCard'

const ExampleComponent: FC<{}> = () => (
  <Page theme={pageTheme.tool}>
    <Header title="Welcome to services!" subtitle="Optional subtitle">
      <HeaderLabel label="Owner" value="Team X" />
      <HeaderLabel label="Lifecycle" value="Alpha" />
    </Header>
    <Content>
      <ContentHeader title="Plugin title">
        <SupportButton>A description of your plugin goes here.</SupportButton>
      </ContentHeader>
      <Grid container spacing={3} direction="column">
        <ServiceCard />
        <Grid item>
          <InfoCard title="Information card">
            <Typography variant="body1">
              All content should be wrapped in a card like this.
            </Typography>
          </InfoCard>
        </Grid>
        <Grid item>
          <InfoCard title="Example User List (fetching data from randomuser.me)">
            <ExampleFetchComponent />
          </InfoCard>
        </Grid>
      </Grid>
    </Content>
  </Page>
)

export default ExampleComponent
