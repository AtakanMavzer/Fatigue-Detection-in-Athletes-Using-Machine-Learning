const express = require('express');
const router = express.Router();
const {authorize} = require('../middleware/authMiddleware');
const {loginUser,getUserData,registerUser} = require('../controllers/userController');

router.post('/',registerUser);
router.post('/login',loginUser);
router.get('/data',getUserData);
//router.get('/data',authorize,getUserData);

module.exports = router