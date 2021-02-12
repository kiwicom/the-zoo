import { Client, dedupExchange, fetchExchange } from 'urql';
import { cacheExchange } from '@urql/exchange-graphcache';
import { relayPagination } from '@urql/exchange-graphcache/extras';
import { Connection, Edge, Node } from './queries';
import { useApi, configApiRef } from '@backstage/core';

const cache = cacheExchange({
  resolvers: {
    Query: {
      services: relayPagination(),
    },
  },
});


function getToken(): string {
    const value = localeStorage.getItem("the-zoo.api.token");
    if (!value) return "";
    const token = JSON.parse(value)["token"];
    return token ? token : "";
}

export const theZooClient = new Client({
  url: '/graphql',
  exchanges: [cache, dedupExchange, fetchExchange],
  fetchOptions: () => {
      let config = useApi(configApiRef);
      let useApiTokenAuth = config.getBoolean("app.useApiTokenAuth");

      if (useApiTokenAuth) {
          const token: string = getToken();
          return {
              headers: { Authorization: token ? `Bearer ${token}` : '' },
          };
      }

      return {};
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

/**
 * Extract the object pk from the Relay base64-encoded id.
 *
 * @param {Node} node The GraphQL object to get the pk/id from
 * @returns {string} The primary key as a string
 */
export function pk(node: Node): string {
  const pk = atob(node.id).split(`${node.__typename}:`)[1];
  if (pk !== parseInt(pk, 10).toString()) {
    throw new Error("This object ID does not represent an integer")
  }
  return pk
}
