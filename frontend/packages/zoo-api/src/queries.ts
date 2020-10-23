export const getServices = `
{
  services(first: 10) {
    edges {
      node {
        id
        name
        owner
        status
        impact
        slackChannel
        pagerdutyService
        pagerdutyInfo {
          id
          summary
          htmlUrl
          oncallPerson {
            type
            summary
            htmlUrl
          }
          pastWeekTotal
        }
        docsUrl
        repository {
          id
          remoteId
          name
          owner
          url
          issues {
            edges {
              node {
                kindKey
                status
                remoteIssueId
                comment
                lastCheck
              }
            }
          }
        }
      }
    }
  }
}
`;

export const getService = `
query ($id: ID!)
  {
    service (id: $id) {
      id
      name
      owner
      status
      impact
      slackChannel
      pagerdutyService
      sentryStats {
        weeklyEvents
        weeklyUsers
        issues {
          edges {
            node {
              category
              culprit
              events
              permalink
              shortId
              title
              users
            }
          }
        }
      }
      docsUrl
      repository {
        id
        remoteId
        name
        owner
        url
        issues {
          edges {
            node {
              kindKey
              status
              remoteIssueId
              comment
              lastCheck
            }
          }
        }
      }
    }
  }
`;

export const getPagerdutyService = `
query ($id: ID!)
  {
    service (id: $id) {
      id
      name
      pagerdutyService
      pagerdutyInfo {
        id
        summary
        htmlUrl
        pastWeekTotal
        allActiveIncidents {
          pageInfo {
            hasNextPage
            hasPreviousPage
            endCursor
            startCursor
          }
          totalCount
          edges {
            node {
              id
              createdAt
              status
              summary
              description
              htmlUrl
              color
            }
          }
        }
        oncallPerson {
          id
          type
          summary
          htmlUrl
        }
      }
    }
  }
`;

export const getIssues = `
  query ($repositoryName: String)
  {
    issues (repositoryName: $repositoryName) {
      kindKey
      status
      remoteIssueId
      comment
      lastCheck
    }
  }
`;

export const getCheckResults = `
  query ($serviceName: String) {
    checkResults (service: $serviceName) {
      kindKey
      title
      description
    }
  }
`


export type Connection = {
  edges: Edge[]
}

export type Edge = {
  __typename: string;
  node: object;
}

export type Service = {
  id: string,
  owner: string;
  name: string;
  status: string;
  impact: string;
  ratingGrade: string;
  ratingReason: string;
  slackChannel: string;
  pagerdutyService: string;
  pagerdutyInfo: PagerdutyInfo;
  sentryStats: SentryStats;
  docsUrl: string;
  repository: Repository;
};

export type Repository = {
  id: string;
  remoteId: number;
  name: string;
  owner: string;
  url: string;
  issues: Issue[];

}

export type Issue = {
  id: string;
  kindKey: string;
  status: string;
  remoteIssueId: string;
  comment: string;
  lastCheck: string;
}

export type CheckResult = {
  kindKey: string;
  // isFound: boolean;
  // status: Field
  // severity: Field
  // effort: Field
  // details:
  title: string;
  description: string;
}

export type PagerdutyInfo = {
  id: string;
  summary: string;
  htmlUrl: string;
  oncallPerson: OncallPerson;
  pastWeekTotal: number;
  allActiveIncidents: ActiveIncident[];
}

export type SentryStats = {
  weeklyEvents: number
  weeklyUsers: number;
  issues: Connection;
}

export type SentryIssue = {
  id: string;
  category: string;
  culprit: string;
  events: number;
  permalink: string;
  shortId: string;
  title: string;
  users: number;
}

export type OncallPerson = {
  id: string;
  type: string;
  summary: string;
  htmlUrl: string;
}

export type ActiveIncident = {
    id: string
    summary: string
    description: string
    status: string
    htmlUrl: string
    createdAt: string
    color: string
}
