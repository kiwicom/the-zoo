import Accordion from "@material-ui/core/Accordion";
import AccordionSummary from "@material-ui/core/AccordionSummary";
import ExpandMoreIcon from "@material-ui/icons/ExpandMore";
import Typography from "@material-ui/core/Typography";
import AccordionDetails from "@material-ui/core/AccordionDetails";
import Grid from "@material-ui/core/Grid";
import React from "react";
import {Card, CardContent, Chip, Link} from "@material-ui/core";
import {Link as RouterLink} from "react-router-dom";


// interface Repo {
//   repoName: string;
//   repoAbsoluteUrl: string;
//   repoOwner: string;
//   repoOwnerUrl: string;
//   status: string;
//   impact: string;
// }
//
// interface Versions {
//   version: string;
//   repos: Repo[]
// }


const VersionList = (versionList) => {
  const versions = versionList.versionList
  console.log(versions)

  return (
    <>
      {versions.map(version => (
          <Accordion key={version.version}>
            <AccordionSummary
              expandIcon={<ExpandMoreIcon />}
              aria-controls={`${version.version}-content`}
              id={`${version.version}-header`}
            >
              <Chip label={version.version} />
            </AccordionSummary>
            <AccordionDetails>
              <Grid container spacing={3} direction="column">
                {version.versionList.edges.map(repo => (
                  <Grid item key={repo.node.id}>
                    <Card>
                      <CardContent>
                        <Grid container direction="row" justify="space-between" alignItems="center">
                          <Grid item>
                            <Grid container alignItems="baseline">
                              <Grid item>
                                <Typography variant="h5">
                                  <Link component={RouterLink} to={`/resources/dependencies/${repo.node.id}`}>{repo.node.repoName}</Link>
                                </Typography>
                              </Grid>
                              <Grid item>
                                owned by&nbsp;{repo.node.repoOwner}
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
