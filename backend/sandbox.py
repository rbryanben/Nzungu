from dotenv import load_dotenv
load_dotenv()

import boto3
import os 
from uuid import uuid4
from datetime import datetime


# params 
reagion = os.getenv('AWS_REAGION')


"""
    Dynamo DB
"""
dynamo_db = boto3.client('dynamodb',region_name=reagion)

# Put a record
reference = str(uuid4())
dynamo_db.put_item(
    TableName=os.getenv("DYNAMO_DB_TABLE"),
    Item={
        "auth_token" : {
            "S" : reference
        },
        "username" : {
            "S" : "rbryanben"
        },
        "created" : {
            "S" : datetime.now().isoformat()
        }
    }
)

# Get the item
item = dynamo_db.get_item(
    TableName=os.getenv("DYNAMO_DB_TABLE"),
    Key={
        "auth_token" : {
            "S" : reference
        }
    }
)

pass 