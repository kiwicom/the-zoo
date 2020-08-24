import { Client, dedupExchange, fetchExchange } from 'urql';
import { cacheExchange } from '@urql/exchange-graphcache';
import { relayPagination } from '@urql/exchange-graphcache/extras';
import { Edge, Connection } from './queries';

const cache = cacheExchange({
  resolvers: {
    Query: {
      services: relayPagination(),
    },
  },
});

function getToken(): string {
  const value = localStorage.getItem("the-zoo.api.token");
  if (!value) return "";
  const token = JSON.parse(value)["token"];
  return token ? token : "";
}

export const theZooClient = new Client({
  url: 'http://127.0.0.1:8000/graphql',
  exchanges: [cache, dedupExchange, fetchExchange],
  fetchOptions: () => {
    const token: string = getToken();
    return {
      headers: { Authorization: token ? `Bearer ${token}` : '' },
    };
  }
});


export const unwrap = (connection: Connection) => connection.edges.map((edge: Edge) => edge.node);
