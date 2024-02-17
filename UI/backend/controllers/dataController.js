const asyncHandler = require('express-async-handler')

const Data = require('../models/dataModel')

// @desc    Get data
// @route   GET /api/data
// @access  Private
const getData = asyncHandler(async (req, res) => {
  const data = await Data.find({ user: req.user.id })
  console.log(req.user.id)
  res.status(200).json(data)
})

// @desc    Set data
// @route   POST /api/data
// @access  Private
const setData = asyncHandler(async (req, res) => {
  if (!req.body) {
    res.status(400).json({message: 'Please enter a data'})
  }
  console.log(req)
  const data = await Data.create({
    data: req.body.data,
    playerId: req.body.playerId,
    user: req.user.id,
  })

  res.status(200).json(data)
})

// @desc    Set data
// @route   POST /api/dataAccess
// @access  Public
const setPublicPlayerData = asyncHandler(async (req, res) => {
  if (!req.body) {
    res.status(400).json({message: 'Please enter a data'})
  }
  console.log(req)
  const data = await Data.create({
    data: req.body.data,
    playerId: req.body.playerId,

  })

  res.status(200).json(data)
})

const getPublicPlayerData = asyncHandler(async (req, res) => {
  const data = await Data.find({ playerId: req.body.playerId })
  res.status(200).json(data)
})


// @desc    Update data
// @route   PUT /api/data/:id
// @access  Private
const updateData = asyncHandler(async (req, res) => {
  const data = await Data.findById(req.params.id)
  if (!data) {
    res.status(400).json({message: 'Data not found'})
  }
  // Check for user
  if (!req.user) {
    res.status(401).json({message: 'User not found'})
  }
  // Make sure the logged in user matches the data user
  if (data.user.toString() !== req.user.id) {
    res.status(401).json({message: 'User not authorized'})
  }
  const updatedData = await Data.findByIdAndUpdate(req.params.id, req.body, {
    new: true,
  })
  res.status(200).json(updatedData)
})

// @desc    Delete data
// @route   DELETE /api/data/:id
// @access  Private
const deleteData = asyncHandler(async (req, res) => {
  const data = await Data.findById(req.params.id)

  if (!data) {
    res.status(400).json({message: 'Data not found'})
  }

  // Check for user
  if (!req.user) {
    res.status(401).json({message: 'User not found'})
  }

  // Make sure the logged in user matches the data user
  if (data.user.toString() !== req.user.id) {
    res.status(401).json({message: 'User not authorized'})
  }

  await data.remove()

  res.status(200).json({ id: req.params.id })
})

module.exports = {
    setData,
    getData,
    updateData,
    deleteData,
    setPublicPlayerData,
    getPublicPlayerData
}