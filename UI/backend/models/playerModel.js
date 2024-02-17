const mongoose = require('mongoose');

const playerSchema = new mongoose.Schema({
    user : {
        type: mongoose.Schema.Types.ObjectId,
        required: true,
        ref: 'User'
    },
    playerId : {
        type: String,
        required: true,
    },
    playerName:{
        type: String,
        required: true
    }
},);
module.exports = mongoose.model('Player', playerSchema)
