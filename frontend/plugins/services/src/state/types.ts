export type Settings = { token: string };
export type SettingsState = Settings & {
  showSettings: boolean;
};

export type State = SettingsState;

type SettingsAction =
  | {
      type: 'setCredentials';
      payload: {
        token: string;
      };
    }
  | { type: 'showSettings' }
  | { type: 'hideSettings' };

export type Action = SettingsAction;
