import dotenv from "dotenv"
dotenv.config()

// Libraries
import {io} from "socket.io-client"

// Create the client 
const client = io(`http://173.249.20.22:8000`,{
    extraHeaders: {
        "Authorization" : "live-updates-8d3922b7-cfca-4dd6-8cde-198c0c3649d8"
    }
})

client.on('connect',()=>{
    console.log("client connected to the server ")
    client.emit("on-event",{
        "name" : "Ryan Ben"
    })
    console.log("send message")
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