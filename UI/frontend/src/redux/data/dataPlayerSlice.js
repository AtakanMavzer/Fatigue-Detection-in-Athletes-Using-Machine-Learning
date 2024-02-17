import { createSlice, createAsyncThunk } from '@reduxjs/toolkit'
import dataService from './dataService'

const initialState = {
  data: [],
  isError: false,
  isSuccess: false,
  isLoading: false,
  message: '',
}

export const getPlayerData = createAsyncThunk('data/getPlayerData', async (
    playerId,
    thunkAPI
  ) => {
      try {
        const token = thunkAPI.getState().auth.user.token
        return await dataService.getPlayerData(token, playerId)
      } catch (error) {
        const message =
          (error.response &&
            error.response.data &&
            error.response.data.message) ||
          error.message ||
          error.toString()
        return thunkAPI.rejectWithValue(message)
      }
    }
  )

export const dataPlayerSlice = createSlice({
  name: 'dataPlayer',
  initialState,
  reducers: {
    resetPlayerData: (state) => {
      state.isLoading = false
      state.isSuccess = false
      state.isError = false
      state.message = ''
      state.dataPlayer = []
    },
  },
  extraReducers:{
    [getPlayerData.pending]: (state, action) => {
      state.isLoading = true;
      state.isError = false;
      state.message = null;
    },
    [getPlayerData.fulfilled]: (state, action) => {
      state.isLoading = false;
      state.isSuccess = true;
      state.dataPlayer = action.payload;
    },
    [getPlayerData.rejected]: (state, action) => {
      state.isLoading = false;
      state.isError = true;
    }
  }
})
export const { resetPlayerData } = dataPlayerSlice.actions
export default dataPlayerSlice.reducer