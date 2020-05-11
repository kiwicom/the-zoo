import React, { FC } from 'react'
import { Typography } from '@material-ui/core'
import Button from '@material-ui/core/Button'
import Card from '@material-ui/core/Card'
import CardActions from '@material-ui/core/CardActions'
import CardContent from '@material-ui/core/CardContent'


const ServiceCard: FC<{}> = () => (
  <Card>
      <CardContent>
        <Typography color="textSecondary" gutterBottom>
          Word of the Day
        </Typography>
        <Typography variant="h5" component="h2">
          be · nev · o · lent
        </Typography>
        <Typography color="textSecondary">
          adjective
        </Typography>
        <Typography variant="body2" component="p">
          well meaning and kindly.
          <br />
          {'"a benevolent smile"'}
        </Typography>
      </CardContent>
      <CardActions>
        <Button size="small">Learn More</Button>
      </CardActions>
    </Card>
)

export default ServiceCard
