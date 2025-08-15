import dotenv from "dotenv"
dotenv.config()

// Libraries
import {io} from "socket.io-client"

// Create the client 
const client = io(`http://173.249.20.22:8000`,{
    extraHeaders: {
        "Authorization" : "sandbox-2c06f48c-61d8-4464-bb86-291989a4311b"
    }
})

client.on('connect',()=>{
    console.log("client connected to the server ")
})

client.on('disconnect',payload => {
    console.log(payload)
})

client.on('on-event',(payload) => {
    console.log(payload)
})

client.on('connect_error', (error) => {
  console.error('Socket.IO connection failed:', error.message);
  // You can also inspect error.description or error.data for more details
});
