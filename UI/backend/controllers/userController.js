const jwt = require("jsonwebtoken");
const bcrypt = require("bcryptjs");
const asyncHandler = require("express-async-handler");
const User = require("../models/userModel");

const generateToken = (id) => {
  return jwt.sign({ id }, process.env.JWT_SECRET, {
    expiresIn: process.env.JWT_EXPIRY,
  });
};

// Authenticate user
// Route Post /api/users/login
const loginUser = asyncHandler(async (req, res) => {
  const { email, password } = req.body;
  const user = await User.findOne({ email });
  
  if (!user) {
    return res.status(400).json({
      message: "User does not exist",
    });
  }
  if (await bcrypt.compare(password, user.password)) {
    return res.status(201).json({
      _id: user.id,
      name: user.name,
      email: user.email,
      token: generateToken(user.id),
    });
  } else {
    return res.status(401).json({
      message: "Wrong Password",
    });
  }
  
});

// Get register user
// Route Get /api/users/data
const registerUser = asyncHandler(async (req, res) => {
  const { name, email, password } = req.body;

  if (!name || !email || !password) {
    return res.status(404).json({ message: "User not found" });
  }

  const findUser = await User.findOne({ email });
  if (findUser) {
    return res.status(400).json({ message: "User Already Exists" });
  }

  const salt = await bcrypt.genSalt(10);
  const hashedPassword = await bcrypt.hash(password, salt);

  const user = await User.create({
    name,
    email,
    password: hashedPassword,
  });

  if (user) {
    return res.status(201).json({
      _id: user.id,
      name: user.name,
      email: user.email,
      token: generateToken(user.id),
    });
  } else {
    return res.status(400).json({ message: "Invalid" });
  }
});
// get User information
// Route post /api/users/data
const getUserData = asyncHandler(async (req, res) => {
  User.find({}).then(function (users) {
    res.send(users.map((user) => user._id.toJSON()));
    });
});

module.exports = {
  loginUser,
  getUserData,
  registerUser,
};
