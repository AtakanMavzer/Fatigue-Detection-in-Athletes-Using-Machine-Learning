import React from 'react'
import {
  CDropdown,
  CDropdownHeader,
  CDropdownItem,
  CDropdownMenu,
  CDropdownToggle,
} from '@coreui/react'
import {
  cilLockLocked,
} from '@coreui/icons'
import CIcon from '@coreui/icons-react'
import {useDispatch} from 'react-redux'
import {logout, reset} from '../../redux/auth/authSlice'


const AppHeaderDropdown = () => {
  const dispatch = useDispatch()

  function handleLogout() {
    dispatch(logout())
    dispatch(reset())
    window.location.reload();

  }

  return (
    <CDropdown variant="nav-item">
      <CDropdownToggle placement="bottom-end" className="py-0" caret={false}>
        Account
      </CDropdownToggle>
      <CDropdownMenu className="pt-0" placement="bottom-end">
        <CDropdownHeader>Actions</CDropdownHeader>
        <CDropdownItem onClick={handleLogout}>
          <CIcon icon={cilLockLocked} className="me-2" />
          Logout
        </CDropdownItem>
      </CDropdownMenu>
    </CDropdown>
  )
}

export default AppHeaderDropdown
