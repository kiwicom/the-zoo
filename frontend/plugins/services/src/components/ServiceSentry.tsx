import React from 'react';
import {
  Chip,
  Card,
  CardContent,
  Grid,
  Link,
  Paper,
  SvgIcon,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableRow,
  Typography,
  withStyles, Theme, createStyles
} from '@material-ui/core';
import Numeral from 'numeral';
import { SentryIssue, Service, unwrap } from 'zoo-api';
import ServiceSentryRating from './ServiceSentryRating'
import ServiceSentryHistogram from './ServiceSentryHistogram'
import IssueClassificationTooltip from "./IssueClassificationTooltip";


const StyledTableRow = withStyles((theme: Theme) =>
  createStyles({
    root: {
      '&:nth-of-type(odd)': {
        backgroundColor: theme.palette.action.hover,
      },
    },
  }),
)(TableRow);

interface IssueColors {
  stale: string,
  decaying: string,
  spoiled: string
}

const getChipStyle = (x: string): object => {
  const issue_colors: IssueColors = {
    "stale": "red",
    "decaying": "orange",
    "spoiled": "yellow"
  }

  return { backgroundColor: issue_colors[x as keyof IssueColors] }
}



const ServiceSentry = ({ service }: { service: Service }) => {
  const issues = unwrap<SentryIssue>(service.sentryStats.issues);
  return (
    <Card>
      <CardContent>

        <Grid container direction="row" justify="space-between">
          <Grid item key={service.id}>
            <Grid container direction="row" justify="flex-start">
              <Grid item>
                <SvgIcon viewBox="0 0 50 39" width="24" height="22" >
                  <path fill="#ffffff" d="M29,2.26a4.67,4.67,0,0,0-8,0L14.42,13.53A32.21,32.21,0,0,1,32.17,40.19H27.55A27.68,27.68,0,0,0,12.09,17.47L6,28a15.92,15.92,0,0,1,9.23,12.17H4.62A.76.76,0,0,1,4,39.06l2.94-5a10.74,10.74,0,0,0-3.36-1.9l-2.91,5a4.54,4.54,0,0,0,1.69,6.24A4.66,4.66,0,0,0,4.62,44H19.15a19.4,19.4,0,0,0-8-17.31l2.31-4A23.87,23.87,0,0,1,23.76,44H36.07a35.88,35.88,0,0,0-16.41-31.8l4.67-8a.77.77,0,0,1,1.05-.27c.53.29,20.29,34.77,20.66,35.17a.76.76,0,0,1-.68,1.13H40.6q.09,1.91,0,3.81h4.78A4.59,4.59,0,0,0,50,39.43a4.49,4.49,0,0,0-.62-2.28Z" />
                </SvgIcon>
              </Grid>
              <Grid item>
                <Typography variant="h6">Sentry stats</Typography>
              </Grid>
            </Grid>
          </Grid>
          <Grid item>{service.sentryStats.weeklyEvents} weekly issues | {service.sentryStats.weeklyUsers} users affected</Grid>
        </Grid>
        <ServiceSentryRating grade={service.ratingGrade} reason={service.ratingReason}/>
        <Grid container direction="row" justify="space-between">
          <Grid item>
            <Typography paragraph><strong>Here is a list of the issues that we recommend checking:</strong></Typography>
          </Grid>
          <Grid item>
            <IssueClassificationTooltip/>
          </Grid>
        </Grid>
        <TableContainer component={Paper}>
          <Table aria-label="simple table">
            <TableBody>
              {issues.map((issue, idx) => (
                <StyledTableRow key={`${issue.shortId}-${idx}`}>
                  <TableCell align="left" scope="row"> {issue.shortId} </TableCell>
                  <TableCell>
                    <Link href={issue.permalink}>
                      <strong>{issue.title}</strong>
                    </Link> <br />
                    <Typography color="textSecondary">{issue.culprit}</Typography>
                  </TableCell>
                  <TableCell align="right"><Chip label={issue.category.toLowerCase()} size="small" style={getChipStyle(issue.category.toLowerCase())} /></TableCell>
                  <TableCell align="right"> {Numeral(issue.events).format('0a')} events <br />{issue.users} users </TableCell>
                  <TableCell align="center"><ServiceSentryHistogram width={150} height={40} issue={issue}/></TableCell>
                </StyledTableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>

      </CardContent>
    </Card>
  )
}

export default ServiceSentry;
