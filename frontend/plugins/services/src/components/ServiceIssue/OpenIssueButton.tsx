import { Button , Snackbar } from '@material-ui/core';
import MuiAlert, { AlertProps } from '@material-ui/lab/Alert';
import React, { useState } from 'react';
import { useMutation } from 'urql';
import { Issue, openIssue } from 'zoo-api';


function Alert(props: AlertProps) {
  return <MuiAlert elevation={6} variant="filled" {...props} />;
}


const OpenIssueButton = ({ issue }: { issue: Issue }) => {
  const pageUrl = window.location;
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [, updateOpenIssue] = useMutation(openIssue);

  const handleOpenIssue = async () => {
    setLoading(true);
    const result = await updateOpenIssue({ input: { issueId: issue.id, pageUrl } });
    if (result.error) {
      setError(result.error.message);
      setLoading(false);
    };
    // issue.remoteIssueId is changed but it’s value might not be accessible right now
  }

  return (
    <>
      {
        issue.remoteIssueId
          ? <Button variant="contained" color="primary" component="a" href={`${issue.remoteIssueUrl}`}>See issue {`#${issue.remoteIssueId}`}</Button>
          : <Button variant="contained" color="primary" disabled={loading} onClick={() => handleOpenIssue()}>Open issue</Button>
      }
      <Snackbar open={!!error} autoHideDuration={9000} onClose={() => setError('')} >
        <Alert onClose={() => setError('')} severity="warning">{error}</Alert>
      </Snackbar>
    </>
  )
}

export default OpenIssueButton;
