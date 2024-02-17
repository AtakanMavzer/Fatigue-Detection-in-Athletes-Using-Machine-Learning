import { createSlice, createAsyncThunk } from '@reduxjs/toolkit'
import dataService from './dataService'

const initialState = {
  data: [],
  isError: false,
  isSuccess: false,
  dataIsLoading: false,
  message: '',
}


// Get user data
export const getData = createAsyncThunk('data/getData', async (_, thunkAPI) => {
    try {
      const token = thunkAPI.getState().auth.user.token
      return await dataService.getAllData(token)
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

 

export const dataSlice = createSlice({
  name: 'data',
  initialState,
  reducers: {
    resetData: (state) => {
      state.dataIsLoading = false
      state.isSuccess = false
      state.isError = false
      state.message = ''
      state.data = []
    },
  },
  extraReducers:{
    [getData.pending]: (state, action) => {
      state.dataIsLoading = true;
      state.isError = false;
      state.message = null;
      state.isSuccess = false;
    },
    [getData.fulfilled]: (state, action) => {
      state.dataIsLoading = false;
      state.isSuccess = true;
      state.data = action.payload;
    },
    [getData.rejected]: (state, action) => {
      state.dataIsLoading = false;
      state.isError = true;
      state.message = action.payload;
      state.isSuccess = false;
    }
    
  }
})



export const { resetData } = dataSlice.actions

export default dataSlice.reducer
