import React from 'react'
import CIcon from '@coreui/icons-react'
import {
  cilSpeedometer,
  cilBalanceScale
} from '@coreui/icons'
import {  CNavItem, CNavTitle } from '@coreui/react'

const _nav = [
  {
    component: CNavTitle,
    name: 'Main',
  },
  {
    component: CNavItem,
    name: 'Dashboard',
    to: '/dashboard',
    icon: <CIcon icon={cilSpeedometer} customClassName="nav-icon" />,
    
  }
  

]

export default _nav
