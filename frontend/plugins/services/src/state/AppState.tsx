import React, { useReducer, Dispatch, Reducer } from 'react';
import type { Action, SettingsState, State } from './types';\

export type { SettingsState };

export const AppContext = React.createContext<[State, Dispatch<Action>]>(
  [] as any,
);

const initialState: State = {
  token: '',
  showSettings: false,
};

const reducer: Reducer<State, Action> = (state, action) => {
  switch (action.type) {
    case 'setCredentials':
      return {
        ...state,
        ...action.payload,
      };
    case 'showSettings':
      return { ...state, showSettings: true };
    case 'hideSettings':
      return { ...state, showSettings: false };
    default:
      return state;
  }
};

export const AppStateProvider = ({ children }: { children: React.ReactNode }) => {
  const [state, dispatch] = useReducer(reducer, initialState);
  return (
    <AppContext.Provider value={[state, dispatch]}>
      <>{children}</>
    </AppContext.Provider>
  );
};
