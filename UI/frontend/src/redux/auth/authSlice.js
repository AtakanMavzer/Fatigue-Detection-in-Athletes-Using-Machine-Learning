import {createSlice, createAsyncThunk} from '@reduxjs/toolkit'
import authService from './authService'

const user=JSON.parse(localStorage.getItem('user'));

const initialState = {
    user: user ? user : null,
    isError: false,
    isLoading: false,
    isLoggedIn: false,
    message: null,
};

// Login user
export const login = createAsyncThunk('auth/login', async (user, thunkAPI) => {
    try {
      return await authService.login(user)
    } catch (error) {
      const message =
        ("yes",error.response && error.response.data && error.response.data.message) ||
        error.message ||
        error.toString()
      return thunkAPI.rejectWithValue(message)
    }
})
// logout user
export const logout = createAsyncThunk('auth/logout', async (user, thunkAPI) => {
    try {
      return await authService.logout()
    } catch (error) {
      const message =
        ("yes",error.response && error.response.data && error.response.data.message) ||
        error.message ||
        error.toString()
      return thunkAPI.rejectWithValue(message)
    }
})


export const authSlice = createSlice({
    name: 'auth',
    initialState,
    reducers: {
        reset: (state) => {
          state.isLoading = false
          state.isSuccess = false
          state.isError = false
          state.message = ''
        },
    },
    extraReducers: {
        [login.pending]: (state, action) => {
            state.isLoading = true;
            state.isError = false;
            state.message = null;
        }
        ,
        [login.fulfilled]: (state, action) => {
            state.user = action.payload;
            state.isLoggedIn = true;
            state.isLoading = false;
            state.isError = false;
            state.message = null;
        }
        ,
        [login.rejected]: (state, action) => {
            state.isLoading = false;
            state.isError = true;
            state.message = action.payload;
        }
    }
});
export const { reset } = authSlice.actions
export default authSlice.reducer