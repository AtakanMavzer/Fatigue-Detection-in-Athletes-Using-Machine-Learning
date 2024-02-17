import React, { useEffect } from 'react'
import { AppContent, AppSidebar, AppHeader } from '../components/index'
import { useNavigate } from 'react-router-dom'
import {useDispatch, useSelector} from 'react-redux'
import {getAllPlayers} from '../redux/players/playersSlice'
import {getData} from '../redux/data/dataSlice'

const DefaultLayout = () => {
  const dispatch = useDispatch()
  const navigate = useNavigate()
  const {user} = useSelector((state) => state.auth)
  const {players,isSuccess} = useSelector((state) => state.players)

  useEffect(() => {
    if (!user) {
      console.log("user is not logged in")
      navigate('/login')
      
    }
  }, [user, navigate])

  useEffect(() => {
    if (isSuccess ) {
      console.log("data is loaded")
    }else{
      dispatch(getAllPlayers())
      dispatch(getData())
    }
  }, [players, isSuccess, dispatch])

  return (
    <div>
      <AppSidebar />
      <div className="wrapper d-flex flex-column min-vh-100 bg-light">
        <AppHeader />
        {isSuccess ? ( 
        <div className="body flex-grow-1 px-3">
          <AppContent />
        </div>
        ) : (
          <div>Loading...</div>
            )
            }
      </div>
    </div>
  )
}

export default DefaultLayout
