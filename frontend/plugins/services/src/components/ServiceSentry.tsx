import React, { FC } from 'react';
import {
  Chip,
  Card,
  CardContent,
  Grid,
  Link,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableRow,
  Typography,
  withStyles, Theme, createStyles
} from '@material-ui/core';
import ContactlessIcon from '@material-ui/icons/Contactless';
import InfoIcon from '@material-ui/icons/Info';
import { SentryIssue, Service } from 'zoo-api';
import { unwrap } from 'zoo-api/src/client';

type Props = {
  service: Service;
}

const StyledTableRow = withStyles((theme: Theme) =>
  createStyles({
    root: {
      '&:nth-of-type(odd)': {
        backgroundColor: theme.palette.action.hover,
      },
    },
  }),
)(TableRow);



const ServiceSentry: FC<Props> = ({ service }) => {
  const issues: SentryIssue[] = unwrap(service.sentryStats.issues);
  return (
    <Card>
      <CardContent>

        <Grid container direction="row" justify="space-between">
          <Grid item key={service.id}>
            <Grid container direction="row" justify="flex-start">
              <Grid item><ContactlessIcon /></Grid>
              <Grid item>
                <Typography variant="h6">Sentry stats</Typography>
              </Grid>
            </Grid>
          </Grid>
          <Grid item>{service.sentryStats.weeklyEvents} weekly issues | {service.sentryStats.weeklyUsers} users affected</Grid>
        </Grid>

        <Grid container direction="row">
          <Grid item><InfoIcon style={{ color: 'orange' }} /></Grid>
          <Grid item>
            <Typography> This project has been rated <span role="img" aria-label="B">{service.ratingGrade} — {service.ratingReason}</span> </Typography>
            <Typography paragraph variant="subtitle2">81 issues found, and 9 of them need to be handled 🧐 Come on, we can do better 💪🏻 </Typography>
          </Grid>
        </Grid>

        <Typography paragraph><strong>Here is a list of the issues that we recommend checking:</strong></Typography>
        <TableContainer component={Paper}>
          <Table aria-label="simple table">
            <TableBody>
              {issues.map((issue) => (
                <StyledTableRow key={issue.shortId}>
                  <TableCell align="left" scope="row"> {issue.shortId} </TableCell>
                  <TableCell> <Link href={issue.permalink}>
                    {issue.title}
                  </Link> <br />
                    <Typography variant="subtitle2" color="textSecondary">{issue.culprit}</Typography> </TableCell>
                  <TableCell align="right"><Chip label={issue.category.toLowerCase()} size="small" style={{ backgroundColor: 'orange' }} /></TableCell>
                  <TableCell align="right"> {issue.events} events <br />{issue.users} users </TableCell>
                  <TableCell align="right">graph</TableCell>
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
