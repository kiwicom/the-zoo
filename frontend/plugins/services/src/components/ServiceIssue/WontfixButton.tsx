import { Box, Button, Dialog, DialogTitle, List, ListItem, Snackbar, TextField } from '@material-ui/core';
import MuiAlert, { AlertProps } from '@material-ui/lab/Alert';
import React, { useState } from 'react';
import { useMutation } from 'urql';
import { Issue, setWontfix } from 'zoo-api';

function Alert(props: AlertProps) {
  return <MuiAlert elevation={6} variant="filled" {...props} />;
}

const WontfixButton = ({ issue }: { issue: Issue }) => {
  const [visible, showButton] = useState(true);
  const [comment, setComment] = useState("");
  const [opened, open] = useState(false);
  const [error, setError] = useState("");
  const [, updateWontfix] = useMutation(setWontfix);

  const handleWontfix = async (issue: Issue) => {
    showButton(false);
    open(false);
    const result = await updateWontfix({ input: { issueId: issue.id, comment } });
    if (result.error) {
      setError(result.error.message)
      showButton(true)
    };
    setComment("");
  };

  return (
    <>
      {visible && <Button id={issue.id} variant="outlined" color="secondary" onClick={() => open(true)}>Wontfix</Button>}

      <Dialog open={opened} onClose={() => open(false)}>
        <DialogTitle>Are you sure this shouldn't or can't be fixed?</DialogTitle>
        <form onSubmit={e => {e.preventDefault(); handleWontfix(issue)}}>
          <List>
            <ListItem>
              <TextField
                name={`wontfix-reason-${issue.kind.key}`}
                label="Please describe why"
                fullWidth
                variant="outlined"
                value={comment}
                onChange={e => setComment(e.target.value)}
              />
            </ListItem>
            <ListItem>
              <Box mt={2} display="flex" width="100%" justifyContent="right">
                <Button onClick={() => { setComment(''); open(false); }}>Cancel</Button>
                <Button variant="outlined" color="secondary" type="submit" onClick={() => {handleWontfix(issue)}}>
                  I won't fix
                </Button>
              </Box>
            </ListItem>
          </List>
        </form>
      </Dialog>

      <Snackbar open={!!error} autoHideDuration={9000} onClose={() => setError('')} >
        <Alert onClose={() => setError('')} severity="warning">{error}</Alert>
      </Snackbar>
    </>
  )
}

export default WontfixButton;
