const asyncHandler = require('express-async-handler')


const Players = require('../models/playerModel')

// @route   POST api/players
// @desc    Get all players
// @access  Private
const getUsersPlayers = asyncHandler(async (req, res) => {
    console.log("getUsersPlayers")
    const players = await Players.find({user: req.user.id})
    if(!players) {
        res.status(400).json({message: 'No players found'})
    }
    res.status(200).json(players)
})

// @route   POST api/players
// @desc    Get all players
// @access  Public
const getUsersPlayersPublic = asyncHandler(async (req, res) => {
    const players = await Players.find({user: req.body.id})
    if(!players) {
        res.status(400).json({message: 'No players found'})
    }
    res.status(200).json(players)
})

// @route   POST api/players
// @desc    Set a player
// @access  Private
const setPlayer = asyncHandler(async (req, res) => {
    const player = await Players.create({
        playerName: req.body.playerName,
        playerId: req.body.playerId,
        user: req.body.userId
    })
    if(!player) {
        res.status(400).json({message: 'Player cannot be created'})
    }
    res.status(200).json(player)
})

const setPlayerPublic = asyncHandler(async (req, res) => {
    const player = await Players.create({
        playerName: req.body.playerName,
        playerId: req.body.playerId,
        user: req.body.userId
    })
    if(!player) {
        res.status(400).json({message: 'Player cannot be created'})
    }
    console.log(player)
    res.status(200).json(player)
})

module.exports = {
    getUsersPlayers,
    setPlayer,
    getUsersPlayersPublic,
    setPlayerPublic
}
