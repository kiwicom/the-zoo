import {
  Breadcrumbs,
  Button,
  Card,
  CardContent,
  Grid,
  IconButton,
  Link,
  Tooltip,
  Typography
} from '@material-ui/core';
import BugReportIcon from '@material-ui/icons/BugReport';
import CallSplitIcon from '@material-ui/icons/CallSplit';
import CodeIcon from '@material-ui/icons/Code';
import FilterNoneIcon from '@material-ui/icons/FilterNone';
import PagesIcon from '@material-ui/icons/Pages';
import PersonIcon from '@material-ui/icons/Person';
import StarIcon from '@material-ui/icons/Star';
import React from 'react';
import { getProjectDetails, Repository, useBackend } from 'zoo-api';
import Count from './Count';


const ServiceRepository = ({ repository }: { repository: Repository }) => (
  <Card>
    <CardContent>
      <Grid container direction="row" justify="space-between">

        <Grid item>
          <Grid container direction="row" >
            <Grid item style={{ paddingTop: '12px' }}><PagesIcon /></Grid>
            <Grid item>
              <Breadcrumbs>
                <Link href={repository.url.slice(0, repository.url.lastIndexOf('/'))} target="_blank" rel="noopener">
                  <Typography variant="h6" color="textPrimary">{repository.owner}</Typography>
                </Link>
                <Link href={repository.url} target="_blank" rel="noopener">
                  <Typography variant="h6">{repository.name}</Typography>
                </Link>
              </Breadcrumbs>
            </Grid>
          </Grid>
        </Grid>

        <Grid item>
          <Grid container direction="row" justify="flex-end">
            <Details repo={repository} />

            <Grid item><Button startIcon={<CodeIcon />} variant="contained" color="secondary">Open issue</Button></Grid>
          </Grid>
        </Grid>

      </Grid>
    </CardContent>
  </Card>
)


const Details = ({ repo }: { repo: Repository }) => {
  const [repository] = useBackend<Repository>("repository", getProjectDetails, { id: repo.id });

  type Detail = 'stars' | 'forks' | 'branchCount' | 'issueCount' | 'memberCount';
  const count = (key: Detail) => ((repository && repository.projectDetails) ? repository.projectDetails[key] : undefined);

  return (
    <>
      <DetailIcon title="Stars" count={count("stars")} icon={<StarIcon />} />
      <DetailIcon title="Forks" count={count("forks")} icon={<FilterNoneIcon />} />
      <DetailIcon title="Branches" count={count("branchCount")} icon={<CallSplitIcon />} />
      <DetailIcon title="Issues" count={count("issueCount")} icon={<BugReportIcon />} />
      <DetailIcon title="Members" count={count("memberCount")} icon={<PersonIcon />} />
    </>
  )
}

const DetailIcon = ({ title, count, icon }: { title: string, count?: number, icon: React.ReactNode | null }) => (
  <Grid item>
    <Tooltip placement="top" title={title}>
      <IconButton> {count ? <Count value={count}>{icon}</Count> : icon} </IconButton>
    </Tooltip>
  </Grid>
)

export default ServiceRepository;
