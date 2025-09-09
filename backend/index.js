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