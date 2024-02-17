const express = require('express');
const router = express.Router();
const {authorize} = require('../middleware/authMiddleware');
const {getUsersPlayers,setPlayer,getUsersPlayersPublic,setPlayerPublic} = require('../controllers/playersController');

router.post('/set',authorize,setPlayer);
router.get('/get',authorize,getUsersPlayers);
router.post('/setPublic',setPlayerPublic);
router.post('/getPublic',getUsersPlayersPublic);

module.exports = router;