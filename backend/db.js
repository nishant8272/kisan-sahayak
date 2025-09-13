const mongoose = require('mongoose');

const signupschema = new mongoose.Schema({
    username: String,
    email: {type: String, unique: true},
    password: String,
});

const User = mongoose.model('User', signupschema);

module.exports = User;