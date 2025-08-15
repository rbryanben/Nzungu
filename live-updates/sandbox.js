import dotenv from "dotenv"
dotenv.config()

// Libraries
import {DynamoDBClient, GetItemCommand,PutItemCommand} from "@aws-sdk/client-dynamodb"
import { SNSClient,SubscribeCommand,PublishCommand } from "@aws-sdk/client-sns"




// Attributes 
const AWS_REAGION = process.env.AWS_REAGION
const DYNAMO_DB_TABLE = process.env.DYNAMO_DB_TABLE

// Create the client 
const dynamo_db = new DynamoDBClient({region:AWS_REAGION})
const sns_client = new SNSClient({region: AWS_REAGION }) 

// Publish to a topic
const publish_command = new PublishCommand({
    TopicArn: process.env.LIVE_UPDATES_TOPIC_SNS_ARN,
    Message: JSON.stringify({
        event : "shop-sale",
        payload : {
            shop: "southly-park",
            timestamp: "2025-08-14T10:01:27.261740",
            commited: true
        } 
    })
})

try{
    await sns_client.send(publish_command)
}
catch(error){
    console.log(error)
}



// Write something 
const put_query = {
    TableName : DYNAMO_DB_TABLE,
    Item : {
        auth_token : {
            S : 'sandbox-2c06f48c-61d8-4464-bb86-291989a4311b'
        },
        active : {
            BOOL : true
        },
        created : {
            S : '2025-08-14T10:01:27.261740'
        },
        username : {
            S : 'rben'
        }
    }
}

// Write the query 
let command = new PutItemCommand(put_query)
let response = await dynamo_db.send(command)

// Get the item 
const get_query = {
    TableName : DYNAMO_DB_TABLE,
    Key: {
        auth_token : {
            S : put_query.Item.auth_token.S
        }
    }
}

// Execute the command
command = new GetItemCommand(get_query)
response = await dynamo_db.send(command)

console.log(response)