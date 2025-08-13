import dotenv from 'dotenv'
dotenv.config()

// Libraries
import express from 'express';
import { createServer } from 'node:http';
import { Server } from 'socket.io';
import ioHandler from './handlers.js'
import logMessage from './utils/logger.js';
import { authorization_required } from './middleware.js';


// Expess Server
const app = express();
const server = createServer(app);
const PORT = process.env.PORT

// Socket IO server with CORS enabled
const io = new Server(server, {
  cors: {
    origin: '*', 
    methods: ['GET', 'POST'], 
    allowedHeaders: ['Content-Type']
  }
});

// Home handler 
app.get('/', (req, res) => {
  res.send('Seems like you want tea from a coffee machine! :PS Live updates services');
});

// Middleware 
io.use(authorization_required)

// io handlers
io.on('connection',ioHandler);

// Listen 
server.listen(PORT, () => {
    logMessage(`Server started listening on 0.0.0.0:${PORT}`)
});
