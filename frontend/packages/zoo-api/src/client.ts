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

export const theZooClient = new Client({
  url: '/graphql',
  exchanges: [cache, dedupExchange, fetchExchange],
});


export const unwrap = (connection: Connection) => connection.edges.map((edge: Edge) => edge.node);
