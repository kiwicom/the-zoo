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
        pagerdutyService {
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
      pagerdutyService {
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
  pagerdutyService: PagerdutyService;
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

export type PagerdutyService = {
  summary: string;
  html_url: string;
  oncall_person: OncallPerson;
  past_week_total: number;
}

export type OncallPerson = {
  type: string;
  summary: string;
  html_url: string;
}
