import dotenv from "dotenv"
dotenv.config()
import logMessage from "./utils/logger.js";

// Attributes
const ADMIN_CREDENTIALS = process.env.ADMIN_KEY

// Method to handle onDisconnect
const onDisconnect = (socket) => {
  const clientIp = socket.request.headers['x-forwarded-for'] || socket.request.connection.remoteAddress;
  const clientPort = socket.request.connection.remotePort;
  logMessage(`Client disconnected from socket ${clientIp}:${clientPort}`)
}

// Method to handle onEvent
const onEvent = (socket, payload) => {
    // Authorization
    const authorization = socket.handshake.headers.authorization || socket.handshake.headers.Authorization;
    
    if (authorization !== ADMIN_CREDENTIALS){
      return
    }
    
    // Broadcast only if the client is an admin
    socket.broadcast.emit("on-event",payload)
}

// Method to handle on-connect
export default function onConnection(socket) {

  // Capture client's IP and port on connection
  const clientIp = socket.request.headers['x-forwarded-for'] || socket.request.connection.remoteAddress;
  const clientPort = socket.request.connection.remotePort;

  // Log that the client has connected to the server
  logMessage(`Client connected to socket ${clientIp}:${clientPort}`);

  // Mappings 
  socket.on('disconnect', () => onDisconnect(socket));
  socket.on('on-event', (payload) => onEvent(socket, payload));
}
