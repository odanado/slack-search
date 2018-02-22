import uuid from 'uuid';
import queryString from 'query-string';

import { setSecret } from './auth';

const getOptions = () => {
  const state = uuid.v4();
  setSecret(state);
  return {
    client_id: process.env.SLACK_CLIENT_ID,
    state,
    redirect_uri: `${process.env.SERVER_URL}/callback`,
    scope: 'identify',
  };
};

export const getOAuthSlackUrl = () => {
  const options = getOptions();
  const SLACK_AUTHORIZE_URL = 'https://slack.com/oauth/authorize';
  const url = `${SLACK_AUTHORIZE_URL}?${queryString.stringify(options)}`;
  return url;
};
