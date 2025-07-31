from django.http import JsonResponse
import os
from datetime import datetime
from uuid import uuid4
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import boto3
import logging
from .decorators import authorization_required, json_required
from . import models

# Logging configuration
logging.basicConfig(
    filename='app.log',
    level=logging.INFO
)

# PARAMETERS 
FILE_S3_BUCKET = os.getenv("FILE_S3_BUCKET")
AWS_REAGION = os.getenv('AWS_REAGION')
DYNAMO_DB_TABLE = os.getenv('DYNAMO_DB_TABLE')

# AWS clients 
s3 = boto3.client('s3')
dynamo_db = boto3.client('dynamodb',region_name=AWS_REAGION)

def health(request):
    return JsonResponse({
        "application" : os.getenv("APPLICATION_NAME"),
        "timestamp" : datetime.now().isoformat()
    },safe=False)

@csrf_exempt
@require_http_methods(["POST"])
@json_required(keys={'username','password'})
def authenticate(request):
    # Request reference 
    ref = str(uuid4()) 
    
    # Get the username and password
    username = request.json_body['username']
    password = request.json_body['password']
    user = models.User.getUserByUsername(username)
    
    # check if the credentials are correct
    if not user or not user.check_password(password):
        return JsonResponse({
            "error" : "Invalid credentials",
            "timestamp" : datetime.now().isoformat()
        },safe=False,status=401)
    
    # Disabled user
    if not user.active:
        return JsonResponse({
            "error" : "This user is disabled",
            "timestamp" : datetime.now().isoformat()
        },safe=False,status=403)
            
    
    # Create an auth token
    auth_token = f"auth-token-{uuid4()}"
    
    # save the token to dynamo db
    try:
        dynamo_db.put_item(
            TableName= DYNAMO_DB_TABLE,
            Item = {
                "auth_token" : {
                    "S" : auth_token
                },
                "username" : {
                    "S" : user.username
                },
                "active" : {
                    "BOOL" : user.active
                },
                "created" : {
                    "S" : datetime.now().isoformat()
                }
            }
        )
    except Exception as e:
        logging.error(f'{ref} - Failed to write authorization token to dynamodb - {e}')
        return JsonResponse({
            "error" : "AWS dependency error",
            "ref" : ref,
            "timestamp" : datetime.now().isoformat()
        },safe=False,status=524)
    
    # Return the auth token 
    return JsonResponse({
        "token" : auth_token,
        "ref" : ref,
        "timestamp" : datetime.now().isoformat()
    },safe=False)
    

@csrf_exempt
@require_http_methods(["POST"])
@authorization_required
def file_upload(request):
    # Request reference 
    ref = str(uuid4()) 
    
    # Check if the file is present in the request
    if 'file' not in  request.FILES:
        logging.info(f"{ref} - 'file' key is not defined in the request")
        
        # Response
        return JsonResponse({
            "error" : "'file' key is not defined in the request",
            "ref" : ref,
            "timestamp" : datetime.now().isoformat()
        },safe=True,status=400)
    
    # Get the file and check the size
    file = request.FILES['file']
    max_file_size = int(os.getenv("MAX_FILE_UPLOAD_SIZE"))
    
    # filter size 
    if file.size > max_file_size:
        logging.info(f"{ref} - file too large")
        return JsonResponse({
            "error" : f"file too large - max {max_file_size} bytes",
            "ref" : ref,
            "timestamp" : datetime.now().isoformat()
        })
    
    # Upload to s3
    extension = file.name.split(".")[-1]
    filename = f'{ref}.{extension}'
    key = f"uploads/{filename}"
    
    try:
        s3.upload_fileobj(file,FILE_S3_BUCKET,key)
    except Exception as e:
        logging.error(f'{ref} - Failed to upload file to s3 - {e}')
        return JsonResponse({
            'error' : 'Failed to upload file to s3 buckets',
            'ref' : ref,
            "timestamp" : datetime.now().isoformat()
        })
        
    # Draft the url
    file_url = f"https://{FILE_S3_BUCKET}.s3.amazonaws.com/{key}"
        
    return JsonResponse({
        "filename" : filename,
        "url" : file_url,
        "ref" : ref,
        "timestamp" : datetime.now().isoformat()
    })
    
