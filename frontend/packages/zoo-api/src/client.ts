import { Client, dedupExchange, fetchExchange } from 'urql';
import { cacheExchange } from '@urql/exchange-graphcache';
import { relayPagination } from '@urql/exchange-graphcache/extras';
import { Connection, Edge } from './queries';

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

/**
 * Unwraps objects of type T from a connection edges.
 *
 * @param {Connection} connection - A GraphQL Relay connection field
 * @returns {Array<T>} Where T is the defined type (Service, Issue...)
 */
export function unwrap<T>(connection: Connection<T>): Array<T> {
  return connection.edges.map((edge: Edge<T>) => edge.node);
}
