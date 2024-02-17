import { createSlice, createAsyncThunk } from '@reduxjs/toolkit'
import playersService from './playersService'

const initialState = {
    players: [],
    isError: false,
    isSuccess: false,
    isLoading: false,
    message: '',
}

export const getAllPlayers = createAsyncThunk('players/getAllPlayers', async (_,thunkAPI) => {
    console.log('getPlayers')
    try {
        const token = thunkAPI.getState().auth.user.token
        console.log(token)
        return await playersService.getAllPlayers(token)
    } catch (error) {
        const message =

            (error.response &&
                error.response.data &&
                error.response.data.message) ||
            error.message ||
            error.toString()
        return thunkAPI.rejectWithValue(message)
    }
})


export const playersSlice = createSlice({
    name: 'players',
    initialState,
    reducers: {
        resetPlayers: (state) => {
            state.isLoading = false
            state.isSuccess = false
            state.isError = false
            state.message = ''
            state.players = []
        },
    }, 
    extraReducers: {
        [getAllPlayers.pending]: (state, action) => {
            state.isLoading = true;
            state.isError = false;
            state.message = null;
        },
        [getAllPlayers.fulfilled]: (state, action) => {
            state.isLoading = false;
            state.isSuccess = true;
            state.players = action.payload;
        },
        [getAllPlayers.rejected]: (state, action) => {
            state.isLoading = false;
            state.isError = true;
            state.message = action.payload;
        }

    }
    
    
})

export const { resetPlayers } = playersSlice.actions
export default playersSlice.reducer

