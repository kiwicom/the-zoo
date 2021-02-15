export const getResources = ``

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
        ratingGrade
        ratingReason
        slackChannel
        pagerdutyService
        docsUrl
        repository {
          id
          remoteId
          name
          owner
          url
        }
      }
    }
  }
}
`;

export const getProjectDetails = `
query ($id: ID!)
  {
    repository (id: $id) {
      projectDetails {
        id
        name
        description
        avatar
        url
        readme
        stars
        forks
        branchCount
        memberCount
        issueCount
        lastActivityAt
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
      ratingGrade
      ratingReason
      slackChannel
      pagerdutyService
      environments {
        edges {
          node {
            id
            name
            healthCheckUrl
            dashboardUrl
            logsUrl
            openApiUrl
          }
        }
      }
      sentryStats {
        weeklyEvents
        weeklyUsers
        issues {
          edges {
            node {
              id
              category
              culprit
              events
              permalink
              shortId
              title
              users
              histogram {
                edges {
                  node {
                    id
                    name
                    value
                  }
                }
              }
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
              id
              kindKey
              status
              remoteIssueId
              remoteIssueUrl
              comment
              lastCheck
              kind {
                id
                key
                category
                description
                effort
                namespace
                patch
                severity
                title
              }
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
      patchPreview
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

export const setWontfix = `mutation ($input: SetWontfixInput!) {
  setWontfix(input: $input) {
    issue {
      id
      status
      comment
      kind {
        id
        key
        title
      }
    }
  }
}`

export const openIssue = `mutation ($input: OpenIssueInput!) {
  openIssue(input: $input) {
    issue {
      id
      status
      comment
      remoteIssueId
      remoteIssueUrl
      kind {
        id
        key
        title
      }
    }
  }
}`

export const applyPatches = `mutation ($input: ApplyPatchesInput!) {
  applyPatches(input: $input) {
    issue {
      id
      status
      comment
      remoteIssueId
      remoteIssueUrl
      kind {
        id
        key
        title
      }
    }
  }
}`


interface Node {
  __typename: string,
  id: string,
}

export type Connection<T> = {
  edges: Edge<T>[]
  totalCount: number
}

export type Edge<T> = {
  __typename: string;
  node: T;
}

export interface Service extends Node {
  owner: string;
  name: string;
  status: string;
  impact: string;
  ratingGrade: string;
  ratingReason: string;
  slackChannel: string;
  pagerdutyService: string;
  pagerdutyInfo: PagerdutyInfo;
  sentryStats: SentryStats;
  docsUrl: string;
  repository: Repository;
  environments: Connection<Environment>
}

export interface Repository extends Node {
  remoteId: number;
  name: string;
  owner: string;
  url: string;
  projectDetails: ProjectDetails;
  issues: Connection<Issue>;
}

export interface ProjectDetails {
    id: string;
    name: string;
    description: string;
    avatar: string;
    url: string;
    readme: string;
    stars: number;
    forks: number;
    branchCount: number;
    issueCount: number;
    memberCount: number;
    lastActivityAt: Date;
}

export interface Environment extends Node {
  name: string;
  healthCheckUrl: string;
  dashboardUrl: string;
  logsUrl: string;
  openApiUrl: string;
}

export interface Kind extends Node {
  key: string;
  category: string;
  description: string;
  effort: string;
  namespace: string;
  patch: string;
  severity: string;
  title: string;
}

export enum IssueStatus {
  NEW = "NEW",
  FIXED = "FIXED",
  WONTFIX = "WONTFIX",
  NOT_FOUND = "NOT_FOUND",
  REOPENED = "REOPENED",
}

export interface Issue extends Node {
  kindKey: string;
  kind: Kind;
  status: IssueStatus;
  remoteIssueId: string;
  remoteIssueUrl: string;
  comment: string;
  lastCheck: string;
  patchPreview: string;
}

export interface PagerdutyInfo extends Node {
  summary: string;
  htmlUrl: string;
  oncallPerson: OncallPerson;
  pastWeekTotal: number;
  allActiveIncidents: Connection<ActiveIncident>;
}

export interface SentryStats extends Node {
  keys: string;
  weeklyEvents: number
  weeklyUsers: number;
  issues: Connection<SentryIssue>;
}

export interface HistogramItem extends Node {
  value: number;
  name: string;
}

export interface SentryIssue extends Node {
  category: string;
  culprit: string;
  events: number;
  permalink: string;
  shortId: string;
  title: string;
  users: number;
  histogram: Connection<HistogramItem>;
}

export interface OncallPerson extends Node {
  type: string;
  summary: string;
  htmlUrl: string;
}

export interface ActiveIncident extends Node {
  summary: string;
  description: string;
  status: string;
  htmlUrl: string;
  createdAt: string;
  color: string;
}

export interface Resource extends Node {
  name: string;
  type: string;
  healthStatus: boolean;
  timestamp: string;
  license: string;
  usageCount: number;
  version: string;
}




export const DummyResponse = {
  data: {
    error: undefined,
    extensions: undefined,
    fetching: false,
    resources: {
      edges: [
        {
          node: {
            id: "U2VydmljZTox",
            name: "kiwi-json",
            version: "0.7.0",
            type: "Javascript Library",
            healthStatus: true,
            timestamp: "",
            license: "public",
            usageCount: 54,
          }
        },
        {
          node: {
            id: "U2VydmljZT9x",
            name: "structlog-config",
            version: "0.18.0",
            type: "Python Library",
            healthStatus: true,
            timestamp: "",
            license: "public",
            usageCount: 4,
          }
        }
      ]
    }

  }
}


export const DummyResourceResponse = {
  data: {

    error: undefined,
    extensions: undefined,
    fetching: false,
    resource: {
      id: "U2VydmljZT9x",
      name: "structlog-config",
      version: "0.18.0",
      type: "Python Library",
      description: "",
      healthStatus: true,
      timestamp: "",
      license: "public",
      usageCount: 4,
      versionList: {
        edges: [
          {
            node: {
              id: "U2VydmljZTox",
              repoName: "rta-tool",
              repoOwner: "jaroslav.sevcik",
            }
          },
          {
            node: {
              id: "U2VydmljZT9x",
              repoName: "sms-manager-api",
              repoOwner: "finance",
            }
          }
        ]
      }
    }

  }
}


