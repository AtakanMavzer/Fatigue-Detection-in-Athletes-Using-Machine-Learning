import { configureStore } from '@reduxjs/toolkit'
import authReducer from './redux/auth/authSlice'
import dataReducer from './redux/data/dataSlice'
import playersReducer from './redux/players/playersSlice'
import dataPlayerReducer from './redux/data/dataPlayerSlice'

export const store = configureStore({
  reducer: {
    auth: authReducer,
    data: dataReducer,
    players: playersReducer,
    dataPlayer: dataPlayerReducer
  },
})
