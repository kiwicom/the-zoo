import React from 'react';
import { Badge, BadgeOrigin } from '@material-ui/core'

const anchorOrigin: BadgeOrigin = {
  vertical: 'bottom',
  horizontal: 'right',
}

interface Props {
  value: number
  children: React.ReactNode
}

const Count = ({ value, children }: Props) => (
  <Badge anchorOrigin={anchorOrigin} badgeContent={value} color="primary">{children}</Badge>
)

export default Count;
