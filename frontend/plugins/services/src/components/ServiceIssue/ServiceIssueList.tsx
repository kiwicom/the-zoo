import { Progress } from '@backstage/core';
import { Breadcrumbs, Grid, Link, Typography } from '@material-ui/core';
import Accordion from '@material-ui/core/Accordion';
import AccordionDetails from '@material-ui/core/AccordionDetails';
import AccordionSummary from '@material-ui/core/AccordionSummary';
import Badge from '@material-ui/core/Badge';
import Card from '@material-ui/core/Card';
import CardActions from '@material-ui/core/CardActions';
import CardContent from '@material-ui/core/CardContent';
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';
import Alert from '@material-ui/lab/Alert';
import React from 'react';
import ReactMarkdown from 'react-markdown';
import { Link as RouterLink, useParams } from 'react-router-dom';
import { useQuery } from 'urql';
import { getService, Issue, IssueStatus, Service, unwrap } from 'zoo-api';
import ContentHeader from '../ContentHeader';
import ServiceLabel from '../ServiceLabel';
import OpenIssueButton from './OpenIssueButton';
import ShowPatchButton from './ShowPatchButton';
import WontfixButton from './WontfixButton';


const ServiceIssue = ({ issue }: { issue: Issue }) => {
  const lastChecked = new Intl.DateTimeFormat("en-GB", { dateStyle: "long", timeStyle: "short" }).format(new Date(issue.lastCheck));

  return (
    <Grid item>
      <Card variant="outlined">
        <CardContent>
          <Grid container direction="row" justify="space-between" alignItems="flex-start">

            <Grid item>
              <Grid container alignItems="baseline">
                <Grid item>
                  <Typography variant="h5">{issue.kind.title}</Typography>
                </Grid>
              </Grid>
              <Grid item>
                <Typography variant="subtitle1">Last checked on {lastChecked}</Typography>
              </Grid>
              <Grid item>
                <ReactMarkdown>{issue.kind.description}</ReactMarkdown>
              </Grid>
            </Grid>

            <Grid item>
              <ServiceLabel name="effort" value={issue.kind.effort} />
              <ServiceLabel name="severity" value={issue.kind.severity} />
            </Grid>

          </Grid>
        </CardContent>

        <CardActions>
          {issue.status !== IssueStatus.WONTFIX && <WontfixButton issue={issue} />}
          <ShowPatchButton issue={issue} />
          <OpenIssueButton issue={issue} />
        </CardActions>

      </Card>
    </Grid>
  )
}


const ServiceIssueList = () => {
  const { id } = useParams();
  const [expanded, setExpanded] = React.useState<string | false>(false);

  const handleChange = (panel: string) => (event: React.ChangeEvent<{}>, isExpanded: boolean) => {
    setExpanded(isExpanded ? panel : false);
  };

  const [response] = useQuery({ query: getService, variables: { id } });

  if (response.fetching) {
    return <Progress />;
  } else if (response.error) {
    if (response.error.message === "[Network] Unauthorized") {
      return <Alert severity="error">Unauthorized. Please check your Zoo token in the Settings.</Alert>;
    }
    return <Alert severity="error">{response.error.message}</Alert>;
  }
  const service: Service = response.data.service;
  const issues = unwrap<Issue>(service.repository.issues);

  // Grouping issues by category name
  const categories = issues.reduce((categories, issue) => {
    const name = issue.kind.category;
    categories[name] = [...categories[name] || [], issue];
    return categories
  }, {} as { [category: string]: Issue[] });

  return (
    <>
      <ContentHeader title={`Audit results for ${service.name}`} />
      <Grid container direction="row" justify="space-between">
        <Grid item>
          <Breadcrumbs aria-label="breadcrumb">
            <Link component={RouterLink} color="inherit" to="/services">
              Services
            </Link>
            <Link component={RouterLink} color="inherit" to={`/services/${service.id}/${service.name}`}>
              {service.name}
            </Link>
            <Typography color="textPrimary">
              Auditing
            </Typography>
          </Breadcrumbs>
        </Grid>
      </Grid>

      {Object.entries(categories).map(([category, issues], index) => {
        return (
          <Accordion square expanded={expanded === category || index === 0} onChange={handleChange(category)} key={category}>
            <AccordionSummary expandIcon={<ExpandMoreIcon />} aria-controls="panel-content" id="panel-header">
              <Badge badgeContent={issues.length} color="primary">
                <Typography variant="h4">{category}</Typography>
              </Badge>
              <Typography>&nbsp;</Typography>
            </AccordionSummary>
            <AccordionDetails>
              <Grid container spacing={1} direction="column">
                {issues.map(issue => <ServiceIssue issue={issue} key={issue.id} />)}
              </Grid>
            </AccordionDetails>
          </Accordion>
        )
      })}
    </>
  )
};

export default ServiceIssueList;
