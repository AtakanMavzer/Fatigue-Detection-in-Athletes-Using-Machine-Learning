import * as React from 'react'
import Button from '@mui/material/Button'
import CssBaseline from '@mui/material/CssBaseline'
import TextField from '@mui/material/TextField'
import Box from '@mui/material/Box'
import Typography from '@mui/material/Typography'
import Container from '@mui/material/Container'
import { createTheme, ThemeProvider } from '@mui/material/styles'
import { withStyles } from '@material-ui/core/styles'
import { useSelector, useDispatch } from 'react-redux'
import { login, reset } from '../../../redux/auth/authSlice'
import {getAllPlayers} from '../../../redux/players/playersSlice'
import {getData} from '../../../redux/data/dataSlice'
import { useEffect } from 'react'
import { useNavigate } from 'react-router-dom'

const theme = createTheme({
  palette: {
    background: {
      default: '#27293d',
    },
  },
})
const WhiteTextTypography = withStyles({
  root: {
    color: '#FFFFFF',
  },
})(Typography)

export default function Login() {

  const navigate = useNavigate()
  const dispatch = useDispatch()

  const { user, isError, isSuccess, message } = useSelector((state) => state.auth)
  useEffect(() => {
    if (isSuccess || user) {
      dispatch(getAllPlayers())
      dispatch(getData())
      navigate('/')
    }

    dispatch(reset())
  }, [user, isError, isSuccess, message, navigate, dispatch])

  

  const handleSubmit = (e) => {
    e.preventDefault()
    const data = new FormData(e.currentTarget)
    const userData = {
      email: data.get('email'),
      password: data.get('password'),
    }
    dispatch(login(userData))
  }

  return (
    <ThemeProvider theme={theme}>
      <Container component="main" maxWidth="xs">
        <CssBaseline />
        <Box sx={{ marginTop: 5 }} />
        <Box sx={{ marginTop: 10, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
          <Box
            component="img"
            sx={{
              height: 350,
              width: 350,
              maxHeight: { xs: 350, md: 350 },
              maxWidth: { xs: 350, md: 350 },
            }}
            alt="The house from the offer."
            src={require('./neurocess.png')}
          />
          <Box sx={{ marginTop: 10 }} />
          <WhiteTextTypography component="h1" variant="h5">
            Login
          </WhiteTextTypography>
          <Box component="form" onSubmit={handleSubmit} noValidate sx={{ mt: 1 }}>
            <TextField
              InputLabelProps={{
                style: { color: '#fff' },
              }}
              inputProps={{ style: { borderColor: 'white', color: 'white' } }}
              margin="normal"
              required
              fullWidth
              id="email"
              label="Email Address"
              name="email"
              autoComplete="email"
              autoFocus
            />
            <TextField
              InputLabelProps={{
                style: { color: '#fff' },
              }}
              inputProps={{ style: { color: 'white' } }}
              margin="normal"
              required
              fullWidth
              color="secondary"
              name="password"
              label="Password"
              type="password"
              id="password"
              autoComplete="current-password"
            />
            <Button type="submit" fullWidth variant="contained" sx={{ mt: 3, mb: 2 }}>
              Login
            </Button>
          </Box>
        </Box>
      </Container>
    </ThemeProvider>
  )
}
