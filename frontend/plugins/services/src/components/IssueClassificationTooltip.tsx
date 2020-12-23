import React from "react";
import ClickAwayListener from "@material-ui/core/ClickAwayListener";
import Icon from "@mdi/react";
import {mdiHelpCircleOutline} from "@mdi/js";
import Tooltip from '@material-ui/core/Tooltip';
import Table from '@material-ui/core/Table';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper';
import {Chip} from '@material-ui/core';
import { makeStyles, createStyles } from '@material-ui/core/styles';
import TableBody from '@material-ui/core/TableBody';
import TableHead from '@material-ui/core/TableHead';
import IconButton from '@material-ui/core/IconButton';


const useStyles = makeStyles(() =>
  createStyles({
    customWidth: {
      maxWidth: 350,
    },
    noMaxWidth: {
      maxWidth: 'none',
    }
  }),
);

const IssueClassificationTooltip = () => {
  const [open, setOpen] = React.useState(false);

  const handleTooltipClose = () => {
    setOpen(false);
  };

  const handleTooltipOpen = () => {
    setOpen(true);
  };

  const classes = useStyles();

  return (
    <div>
      <ClickAwayListener onClickAway={handleTooltipClose}>
        <Tooltip
          classes={{ tooltip: classes.customWidth }}
          placement="left"
          PopperProps={{
            disablePortal: true,
          }}
          onClose={handleTooltipClose}
          open={open}
          disableFocusListener
          disableHoverListener
          disableTouchListener
          title={
            <React.Fragment>
              <h3>
                <strong>Issue clasification</strong>
              </h3>
              <div>
                The classification of the issues is based on the number of days the event has been reported during a
                specific time window.
              </div>
              <br />
              <TableContainer component={Paper}>
                <Table>
                  <TableHead></TableHead>
                  <TableBody>
                    <TableRow>
                      <TableCell><Chip label="stale" size="small" style={{ backgroundColor: 'red' }} /></TableCell>
                      <TableCell>seen 14 out of last 14 days</TableCell>
                    </TableRow>
                    <TableRow>
                      <TableCell><Chip label="decaying" size="small" style={{ backgroundColor: 'orange' }} /></TableCell>
                      <TableCell>seen 7 out of last 14 days</TableCell>
                    </TableRow>
                    <TableRow>
                      <TableCell><Chip label="spoiled" size="small" style={{ backgroundColor: 'yellow' }} /></TableCell>
                      <TableCell>seen 4 out of last 7 days</TableCell>
                    </TableRow>
                    </TableBody>
                </Table>
              </TableContainer>
            </React.Fragment>
          }
          arrow
        >
          <IconButton onClick={handleTooltipOpen}>
            <Icon path={mdiHelpCircleOutline} size={1} />
          </IconButton>
        </Tooltip>
      </ClickAwayListener>
    </div>
  );
}


export default IssueClassificationTooltip;
