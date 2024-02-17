const express = require('express');
const { setData,
    getData,
    updateData,
    deleteData,
    setPublicPlayerData,
    getPublicPlayerData } = require('../controllers/dataController');
const router = express.Router();
const {authorize} = require('../middleware/authMiddleware');
//const {loginUser,getData,registerUser} = require('../controllers/userControllers');

router.post('/',authorize,setData);
router.get('/',authorize,getData);
router.put('/:id',authorize,updateData);
router.delete('/:id',authorize,deleteData);
router.post('/get',getPublicPlayerData);
router.post('/getPlayer',getPublicPlayerData);
router.post('/set',setPublicPlayerData);



module.exports = router