import React from 'react';
import {Outlet, useParams} from "react-router-dom";
import ContentHeader from "./ContentHeader";
import ResourcesHeader from "../ResourcesHeader";
import {Content, Page} from "@backstage/core";
import {Card, CardContent} from "@material-ui/core";

import Grid from '@material-ui/core/Grid';
import { makeStyles, createStyles, Theme } from '@material-ui/core/styles';
import Accordion from '@material-ui/core/Accordion';
import AccordionSummary from '@material-ui/core/AccordionSummary';
import AccordionDetails from '@material-ui/core/AccordionDetails';
import Typography from '@material-ui/core/Typography';
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';
import { PieChart, Pie, Sector, Cell } from 'recharts';


const Detailpage = () => {
  const params = useParams();
  const resourceId = params.id;
  console.log(resourceId)

  const useStyles = makeStyles((theme: Theme) =>
    createStyles({
      root: {
        flexGrow: 1,
      },
      paper: {
        padding: theme.spacing(2),
        textAlign: 'center',
        color: theme.palette.text.secondary,
      },
    }),
  );

  const accordionStyles = makeStyles((theme: Theme) =>
    createStyles({
      root: {
        width: '100%',
      },
      heading: {
        fontSize: theme.typography.pxToRem(15),
        fontWeight: theme.typography.fontWeightRegular,
      },
    }),
  );

  //Get resource
  const resource = {
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
      "0.7.0": [
        {
          "repoName": "fantozzi",
          "repoAbsoluteUrl": "https://zoo.skypicker.com/resources/dependencies/1011/",
          "repoOwner": "finance/payments-in",
          "repoOwnerUrl": "",
          "status": "",
          "impact": ""
        },
        {
          "repoName": "fantozzi1",
          "repoAbsoluteUrl": "https://zoo.skypicker.com/resources/dependencies/1011/",
          "repoOwner": "finance/payments-in",
          "repoOwnerUrl": "",
          "status": "",
          "impact": ""
        },
      ]
    }
  }

  const data = [
    { name: 'Group A', value: 400 },
    { name: 'Group B', value: 300 },
    { name: 'Group C', value: 300 },
    { name: 'Group D', value: 200 },
  ];

  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042'];

  const RADIAN = Math.PI / 180;
  const renderCustomizedLabel = ({ cx, cy, midAngle, innerRadius, outerRadius, percent, index }) => {
    const radius = innerRadius + (outerRadius - innerRadius) * 0.5;
    const x = cx + radius * Math.cos(-midAngle * RADIAN);
    const y = cy + radius * Math.sin(-midAngle * RADIAN);

    return (
      <text x={x} y={y} fill="white" textAnchor={x > cx ? 'start' : 'end'} dominantBaseline="central">
        {`${(percent * 100).toFixed(0)}%`}
      </text>
    );
  };

  const classes = useStyles();
  const accordionClasses = accordionStyles();

  return (
    <>
      <ResourcesHeader title="Kiwi.com resources" description="Libraries, Languages, CI templates" />
      <Page themeId="home">
        <Content>
          <ContentHeader resource={resource} />
            <Outlet />
          <Card>
            <CardContent>
              <Grid container spacing={3}>
                <Grid item xs={6}>
                  <PieChart width={400} height={400}>
                    <Pie
                      data={data}
                      cx={200}
                      cy={200}
                      labelLine={false}
                      label={renderCustomizedLabel}
                      outerRadius={80}
                      fill="#8884d8"
                      dataKey="value"
                    >
                      {data.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                      ))}
                    </Pie>
                  </PieChart>
                </Grid>
                <Grid item xs={6}>

                  { Object.entries(resource.versionList).map(([key,value],i) =>
                    <Accordion>
                      <AccordionSummary
                        expandIcon={<ExpandMoreIcon />}
                        aria-controls="panel1a-content"
                        id="{key}-header"
                      >
                        <Typography className={accordionClasses.heading}>{key}</Typography>
                      </AccordionSummary>
                      <AccordionDetails>
                        <Grid container spacing={3} direction="column">
                            <Grid item key="1">
                              <Typography>
                                Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse malesuada lacus ex,
                                sit amet blandit leo lobortis eget.
                              </Typography>
                            </Grid>
                            <Grid item key="2">
                              <Typography>
                                Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse malesuada lacus ex,
                                sit amet blandit leo lobortis eget.
                              </Typography>
                            </Grid>
                        </Grid>
                      </AccordionDetails>
                    </Accordion>
                  )}
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Content>
      </Page>
    </>
  )
};

export default Detailpage;
