import React, {FC} from "react";
import {Grid, Typography} from "@material-ui/core";
import InfoIcon from "@material-ui/icons/Info";
import Icon from "@mdi/react";
import { mdiAlphaACircle,
  mdiAlphaBCircle,
  mdiAlphaCCircle,
  mdiAlphaDCircle,
  mdiAlphaECircle,
  mdiAlphaFCircle,
  mdiAlphaSCircle,
} from "@mdi/js";

type colorInfo = {
  color: string,
  icon: string
}
interface MappingDict {
  [key: string]: colorInfo;
}
const choiceColors: MappingDict = {
  'S': {'color':'teal', 'icon': mdiAlphaSCircle},
  'A': {'color':'green', 'icon': mdiAlphaACircle},
  'B': {'color':'yellow', 'icon': mdiAlphaBCircle},
  'C': {'color':'yellow', 'icon': mdiAlphaCCircle},
  'D': {'color':'orange', 'icon': mdiAlphaDCircle},
  'E': {'color':'orange', 'icon': mdiAlphaECircle},
  'F': {'color':'red', 'icon': mdiAlphaFCircle},
}

type Props = {
  grade: string;
  reason: string;
}

const ServiceSentryRating: FC<Props> = ({ grade, reason }) => {
  let ratingColor =  "white";
  let ratingIcon =  mdiAlphaSCircle;

  if(grade in choiceColors) {
    ratingColor = choiceColors[grade]["color"];
    ratingIcon = choiceColors[grade]["icon"];
  }

  return (
    <Grid container direction="row">
      <Grid item><InfoIcon style={{ color: ratingColor }} /></Grid>
      <Grid item style={{ paddingRight: 0 }}>
        <Typography>
          <strong style={{ color: ratingColor}} >This project has been rated</strong>
        </Typography>
        <Typography paragraph variant="subtitle2">{reason}</Typography>
      </Grid>
      <Grid item style={{ paddingLeft: 2 }}>
        <Icon path={ratingIcon} size={1} style={{ color: ratingColor }}/>
      </Grid>
    </Grid>
  )
}


export default ServiceSentryRating;
