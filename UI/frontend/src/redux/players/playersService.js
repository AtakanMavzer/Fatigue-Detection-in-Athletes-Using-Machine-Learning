import axios from 'axios'

const API_URL = '/api/players/get/'

const getAllPlayers = async (token) => {
    console.log("insidetoken",token)
    const config = {
        headers: {
          Authorization: `Bearer ${token}`,
        },
    }

    const response = await axios.get(API_URL, config)
    return response.data
}

const playerService = {
    getAllPlayers,
}
  
export default playerService