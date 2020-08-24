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
import { Service } from 'zoo-api';

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

function createData(name: string, calories: number, fat: number, carbs: number, protein: number) {
  return { name, calories, fat, carbs, protein };
}

const rows = [
  createData('SERVICE-AB', 159, 6.0, 24, 4.0),
  createData('SERVICE-AC', 237, 9.0, 37, 4.3),
  createData('SERVICE-AF', 262, 16.0, 24, 6.0),
  createData('SERVICE-AX', 305, 3.7, 67, 4.3),
  createData('SERVICE-AZ', 356, 16.0, 49, 3.9),
];

const ServiceSentry: FC<Props> = ({ service }) => (
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
        <Grid item>{`{n} weekly issues | {n} users affected`}</Grid>
      </Grid>

      <Grid container direction="row">
        <Grid item><InfoIcon style={{ color: 'orange' }} /></Grid>
        <Grid item>
          <Typography> This project has been rated 🅱️ </Typography>
          <Typography paragraph variant="subtitle2">81 issues found, and 9 of them need to be handled 🧐 Come on, we can do better 💪🏻 </Typography>
        </Grid>
      </Grid>

      <Typography paragraph><strong>Here is a list of the issues that we recommend checking:</strong></Typography>
      <TableContainer component={Paper}>
        <Table aria-label="simple table">
          <TableBody>
            {rows.map((row) => (
              <StyledTableRow key={row.name}>
                <TableCell align="left" scope="row"> {row.name} </TableCell>
                <TableCell> <Link href="1">
                  ConnectionRefusedError: [Errno 111] Connect call failed ('172.23.129.109', 5432)
                </Link> <br />
                  <Typography variant="subtitle2" color="textSecondary">service.handlers.ready.readiness</Typography> </TableCell>
                <TableCell align="right"><Chip label="decaying" size="small" style={{ backgroundColor: 'orange' }} /></TableCell>
                <TableCell align="right"> 123 events <br />18 users </TableCell>
                <TableCell align="right">graph</TableCell>
              </StyledTableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

    </CardContent>
  </Card>
)

export default ServiceSentry;
