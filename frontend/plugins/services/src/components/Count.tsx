import React, { FC } from 'react';
import { Badge, BadgeOrigin } from '@material-ui/core'

const anchorOrigin: BadgeOrigin = {
  vertical: 'bottom',
  horizontal: 'right',
}

type Props = {
  value: number;
}

const Count: FC<Props> = ({ value, children }) => (
  <Badge anchorOrigin={anchorOrigin} badgeContent={value} color="primary">{children}</Badge>
)

export default Count;
