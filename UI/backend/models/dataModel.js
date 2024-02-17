const mongoose = require('mongoose');

const dataSchema = new mongoose.Schema({
    playerId : {
        type: String,
        required: true,
        ref: 'Player'
    },
    data:{
        type: Object,
        required: true
    },
    insert_date: {
        type: Date,
        default: Date.now
    }
},);
module.exports = mongoose.model('Data', dataSchema)
