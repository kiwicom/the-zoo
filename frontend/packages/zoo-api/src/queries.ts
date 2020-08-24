export const getServices = `
  {
    services {
      id
      name
      owner
      status
      impact
      slackChannel
      pagerdutyUrl
      docsUrl
      repository {
        id
        remoteId
        name
        owner
        url
        issues {
          kindKey
          status
          remoteIssueId
          comment
          lastCheck
        }
      }
    }
  }
`;

export const getService = `
query ($name: String!)
  {
    service (name: $name) {
      id
      name
      owner
      status
      impact
      slackChannel
      pagerdutyUrl
      docsUrl
      repository {
        id
        remoteId
        name
        owner
        url
        issues {
          kindKey
          status
          remoteIssueId
          comment
          lastCheck
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
  slackChannel: string;
  pagerdutyUrl: string;
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
