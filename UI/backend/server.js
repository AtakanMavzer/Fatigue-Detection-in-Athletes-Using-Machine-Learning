const express = require('express');
const dotenv = require('dotenv').config();
const connectDB = require('./config/db');


connectDB();

//express application
const app = express();
app.use(express.json());
const port = process.env.PORT || 5000;


//middleware
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

//route
app.use('/api/users', require('./routes/userRoutes') );
app.use('/api/data', require('./routes/dataRoutes') );
app.use('/api/players', require('./routes/playersRoutes') );

//start server
app.listen(port, () => console.log(`Server started on port ${port}`));

module.exports = server = app;
