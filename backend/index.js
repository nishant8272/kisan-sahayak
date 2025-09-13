<<<<<<< HEAD
const express = require('express');
const app = express();
const port = process.env.PORT;

app.use(express.json());

app.get('/api/v1/signup', (req, res) => {
    res.json({
        massage: 'Hello from server!',
    });
});

app.get('/api/v1/signin', (req, res) => {
    res.json({
        data: [1, 2, 3, 4, 5],
    });
})

app.listen(port);
=======
require('dotenv').config(); 
const express = require('express');
const z = require('zod');
const { default: mongoose } = require('mongoose');
const User = require('./db');
const app = express();
const bcrypt = require("bcrypt")
const jwt = require("jsonwebtoken")
const PORT = process.env.PORT;

app.use(express.json());

app.post('/api/v1/signup', async(req, res) => {
    const { username, email, password } = req.body;

    // define zod schema for validation
    const signupzod = z.object({
        username: z.string(),
        email: z.string(),
        password: z.string().min(6).max(12),
    })
    const validate = signupzod.safeParse(req.body);
    if(!validate.success){
        return res.status(400).json({ error: validate.error });
    }

    // creating user in db.
    try{
        // here we use bcrypt for hashing password
        const hashpassword = await bcrypt.hash(password, 5)
        await User.create({ username, email, password:hashpassword})
    }catch(err){
        console.log(err)
        return res.status(500).json({error: "Internal server error"})
    }
    res.json({
        massage: 'User created succesfully',
    });
});

app.post('/api/v1/signin', async(req, res) => {
    const { email, password} = req.body

    // creaing zod schema for validation
    const signinzod = z.object({
        email: z.string(),
        password: z.string().min(6).max(12),    
    })
    const validate = signinzod.safeParse(req.body);
    if(!validate.success){
        return res.status(400).json({error: validate.error})
    }

    // checking that user exist in db or not 
    try{
        const user = await User.findOne({email})
        if (!user) {
            return res.status(400).json({ error: "Invalid username or password" });
        }
        const isPasswordValid = await bcrypt.compare(password, user.password);
        if (!isPasswordValid) {
            return res.status(400).json({ error: "Invalid username or password" });
        }
        const token = jwt.sign({userId: user._id}, process.env.JWT_SECRET)
        res.json({
            massage:"User signin successfully",
            token
        });
    }catch(err){
        console.log(err)
        return res.status(500).json({ error: "Internal server error" });
    }
})



async function main(){
    if (process.env.MONGODB_URL === undefined) {
        throw new Error("MONGODB_URL is not defined");
    }
    await mongoose.connect(process.env.MONGODB_URL);
    app.listen(PORT, () => {
        console.log("Server is running on port 3000");
    });
}

main()
>>>>>>> bf9f67c7041dfe441e11c80fe78e9255e34fdf71
