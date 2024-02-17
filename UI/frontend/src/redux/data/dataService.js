import axios from 'axios'

const API_URL = '/api/data/'

const getAllData = async (token) => {
  const config = {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  }

  const response = await axios.get(API_URL, config)
  return response.data
}

const getPlayerData = async (token, playerId) => {
  const config = {
    headers: {
      Authorization: `Bearer ${token}`,
    }
  }
  const data ={
    playerId: playerId
  }
  const response = await axios.post(API_URL+'getPlayer/',data ,config)
  return response.data
}

const dataService = {
  getAllData,
  getPlayerData
}

export default dataService