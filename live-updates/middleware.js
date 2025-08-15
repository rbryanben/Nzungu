import dotenv from "dotenv";
dotenv.config();

import {DynamoDBClient, GetItemCommand} from "@aws-sdk/client-dynamodb"
import logMessage from "./utils/logger.js";

// Attributes 
const AWS_REAGION = process.env.AWS_REAGION
const DYNAMO_DB_TABLE = process.env.DYNAMO_DB_TABLE
const ADMIN_CREDENTIALS = process.env.ADMIN_KEY

// AWS
const dynamoDb = new DynamoDBClient({region: AWS_REAGION})

export const authorization_required = async (socket,next) => {
    // Get the parsed token
    const authorization = socket.handshake.headers.authorization || socket.handshake.headers.Authorization;
    const clientIp = socket.request.headers['x-forwarded-for'] || socket.request.connection.remoteAddress;
    
    // Check if authorization has been included in the headers 
    if (authorization === undefined){
      logMessage(`${clientIp} Authorization failed - missing authorization header`)
      return next(new Error("Authorization header required"))
    }

    // If the key is admin then proceed
    if (authorization === ADMIN_CREDENTIALS){
      return next()
    }

    // Validate the auth token 
    const getQuery = {
      TableName : DYNAMO_DB_TABLE,
      Key: {
          auth_token : {
              S : authorization
          }
      }
    }

    const getCommand = new GetItemCommand(getQuery)
    const res = await dynamoDb.send(getCommand)

    // Invalid authorization key
    if (!('Item' in res)){
      logMessage(`${clientIp} Authorization failed - invalid authorization key - ${authorization}`)
      return next(Error('Invalid authorization key'))
    }

    // Check if token is still valid
    const tokenCreatedDate = new Date(res.Item.created.S.slice(0, 23))
    tokenCreatedDate.setHours(tokenCreatedDate.getHours() + 6);

    if (new Date > tokenCreatedDate){
        logMessage(`${clientIp} Authorization token expired - ${authorization}`)
        return next(Error('Authorization token expired'))
    }

    // Proceed
    logMessage(`${clientIp} Authorized socket connection`)   
    return next()  
}