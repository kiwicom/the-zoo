import Accordion from '@material-ui/core/Accordion';
import AccordionSummary from '@material-ui/core/AccordionSummary';
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';
import Typography from '@material-ui/core/Typography';
import AccordionDetails from '@material-ui/core/AccordionDetails';
import Grid from '@material-ui/core/Grid';
import React from 'react';
import { Card, CardContent, Chip, Link } from '@material-ui/core';
import { Link as RouterLink } from 'react-router-dom';
import { DependencyUsage } from 'zoo-api';


export interface SortedVersions { [key: string]: object[]; }

export const sortDependencyUsages = (versions:DependencyUsage[]) => {
  const sortedVersions:SortedVersions = {}

  for (const version of versions) {
    if(sortedVersions[version.version]){
      sortedVersions[version.version].push(version.repo)
      continue
    }
    sortedVersions[version.version] = [version.repo]
  }

  return sortedVersions
}


const VersionList = ({ activeVersions, dependencyId }: { activeVersions: DependencyUsage[], dependencyId: string }) => {
  const versions = sortDependencyUsages(activeVersions)

  return (
    <>
      {Object.keys(versions).map((version, _) => (
          <Accordion key={version}>
            <AccordionSummary
              expandIcon={<ExpandMoreIcon />}
              aria-controls={`${version}-content`}
              id={`${version}-header`}
            >
              <Chip label={version} />
            </AccordionSummary>
            <AccordionDetails>
              <Grid container spacing={3} direction="column">
                {versions[version].map(repo => (
                  <Grid item key={repo.id}>
                    <Card>
                      <CardContent>
                        <Grid container direction="row" justify="space-between" alignItems="center">
                          <Grid item>
                            <Grid container alignItems="baseline">
                              <Grid item>
                                <Typography variant="h5">
                                  <Link component={RouterLink} to={`/resources/dependencies/${dependencyId}`}>{repo.name}</Link>
                                </Typography>
                              </Grid>
                              <Grid item>
                                owned by&nbsp;{repo.owner}
                              </Grid>
                            </Grid>
                          </Grid>
                        </Grid>
                      </CardContent>
                    </Card>
                  </Grid>
                  ))}
              </Grid>
            </AccordionDetails>
          </Accordion>
          ))}
    </>
  )
}

export default VersionList;
