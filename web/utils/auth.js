import Cookie from 'js-cookie';
import cookie from 'cookie-parse';

export const setToken = (token) => {
  if (process.SERVER_BUILD) return;
  window.localStorage.setItem('token', token);
  Cookie.set('token', token);
};

export const unsetToken = () => {
  if (process.SERVER_BUILD) return;
  window.localStorage.removeItem('token');
  window.localStorage.removeItem('secret');
  Cookie.remove('token');
  window.localStorage.setItem('logout', Date.now());
};

export const getTokenFromCookie = (req) => {
  if (!req.headers.cookie) return undefined;
  const cookies = cookie.parse(req.headers.cookie);
  return cookies.token;
};

export const getTokenFromLocalStorage = () => {
  const { token } = window.localStorage;
  return token;
};


export const setSecret = secret => window.localStorage.setItem('secret', secret);
export const validateSecret = secret => window.localStorage.secret === secret;
