import dotenv from "dotenv"
dotenv.config()

// Libraries
import {io} from "socket.io-client"

// Create the client 
const client = io(`http://127.0.0.1:8000`,{
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

client.on('connect_error', (err) => {
    console.error("Connection failed:", err.message.error);
});