import { Box, Button, Dialog, DialogTitle, List, ListItem, Snackbar } from '@material-ui/core';
import MuiAlert, { AlertProps } from '@material-ui/lab/Alert';
import React, { useState } from 'react';
import { useMutation } from 'urql';
import { applyPatches, Issue } from 'zoo-api';


function Alert(props: AlertProps) {
  return <MuiAlert elevation={6} variant="filled" {...props} />;
}


const ShowPatchButton = ({ issue }: { issue: Issue }) => {
  const [error, setError] = useState("");
  const [opened, open] = useState(false);
  const [loading, setLoading] = useState(false);
  const [, updateApplyPatches] = useMutation(applyPatches);

  const handleApplyPatch = async () => {
    setLoading(true);
    open(false);
    const result = await updateApplyPatches({ input: { issueId: issue.id } });
    if (result.error) {
      setError(result.error.message);
      setLoading(false);
    };
  }

  if (!issue.kind.patch) return null;

  return (
    <>
      <Button variant="contained" color="primary" disabled={loading} onClick={() => { open(true) }}>Show patch</Button>

      <Dialog open={opened} onClose={() => open(false)}>
        <DialogTitle>Here are the proposed changes to fix the issue. </DialogTitle>

        <List>
          <ListItem>
            <div dangerouslySetInnerHTML={{ __html: issue.patchPreview }} />
          </ListItem>
          <ListItem>
            <Box mt={2} display="flex" width="100%" justifyContent="right">
              <Button onClick={() => { open(false) }}>Cancel</Button>
              <Button variant="outlined" color="primary" type="submit" onClick={() => { handleApplyPatch() }}>
                Apply patch
              </Button>
            </Box>
          </ListItem>
        </List>

      </Dialog>

      <Snackbar open={!!error} autoHideDuration={9000} onClose={() => setError('')} >
        <Alert onClose={() => setError('')} severity="warning">{error}</Alert>
      </Snackbar>
    </>
  )
}

export default ShowPatchButton;
