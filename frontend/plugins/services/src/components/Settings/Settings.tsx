import React, { useState, useEffect } from 'react';
import {
  Button,
  TextField,
  List,
  ListItem,
  Snackbar,
  Box,
  Dialog,
  DialogTitle,
} from '@material-ui/core';
import { Alert } from '@material-ui/lab';
import { useSettings } from '../../state';

const Settings = () => {
  const [
    {
      token: tokenFromStore,
      showSettings,
    },
    { saveSettings, hideSettings },
  ] = useSettings();

  const [token, setToken] = useState(() => tokenFromStore);

  useEffect(() => {
    if (tokenFromStore !== token) {
      token ? setToken(token) : setToken(tokenFromStore);
    }
  }, [tokenFromStore, token]);

  const [saved, setSaved] = useState(false);

  return (
    <>
      <Snackbar
        autoHideDuration={1000}
        open={saved}
        anchorOrigin={{ vertical: 'top', horizontal: 'center' }}
        onClose={() => setSaved(false)}
      >
        <Alert severity="success">Credentials saved.</Alert>
      </Snackbar>
      <Dialog open={showSettings} onClose={hideSettings}>
        <DialogTitle>
          Project Credentials
          {/* {authed ? <StatusOK /> : <StatusFailed />} */}
        </DialogTitle>
        <Box minWidth="400px">
          <List>
            <ListItem>
              <TextField
                name="zoo-token"
                label="Token"
                value={token}
                fullWidth
                variant="outlined"
                onChange={e => setToken(e.target.value)}
              />
            </ListItem>
            <ListItem>
              <Box mt={2} display="flex" width="100%" justifyContent="center">
                <Button
                  data-testid="github-auth-button"
                  variant="outlined"
                  color="primary"
                  onClick={() => {
                    setSaved(true);
                    saveSettings({ token });
                    hideSettings();
                  }}
                >
                  Save credentials
                </Button>
              </Box>
            </ListItem>
          </List>
        </Box>
      </Dialog>
    </>
  );
};

export default Settings;
