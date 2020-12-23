import React from "react";
import { SentryIssue } from 'zoo-api';
import { BarChart, Bar, Tooltip } from 'recharts';

const CustomTooltipStyle = {
  backgroundColor: 'rgba(255, 255, 255, 0.8)',
  color: 'rgba(0, 0, 0, 0.87)',
  fontSize: 12,
  paddingRight: 5,
  paddingBottom: 1,
  paddingTop: 1,
  paddingLeft: 5
}

type TooltipProps = {
  active?: boolean;
  payload?: { value: number, payload: { name: string } }[];
}

const HistogramTooltip = ({ active, payload }: TooltipProps) => {
  if (active && payload) {
    return (
      <div style={CustomTooltipStyle}>
        <p><strong>{payload[0].payload.name}</strong></p>
        <p className="content"><strong>{payload[0].value}</strong> events</p>
      </div>
    );
  }

  return null;
};

type Props = {
  issue: SentryIssue;
  width: number;
  height: number;
}

const ServiceSentryHistogram = ({ issue, width, height }: Props) => {
  const data = []
  for (const val of issue.histogram.edges) {
    data.push({ "name": val.node.name, "value": val.node.value })
  }
  return (
    <span style={{ display: "flex", justifyContent: "center" }}>
      <BarChart width={width} height={height} data={data} barCategoryGap={0.1}>
        <Bar dataKey='value' fill='#212121' />
        <Tooltip content={<HistogramTooltip />} />
      </BarChart>
    </span>
  )
}

export default ServiceSentryHistogram;
