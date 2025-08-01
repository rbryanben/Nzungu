from django.http import JsonResponse
import boto3
import os 
import json
from typing import Dict
from datetime import datetime, timedelta
from .models import User
from shared_models import models as shared_models

# AWS paramets 
reagion = os.getenv('AWS_REAGION')
dynamo_db_table = os.getenv('DYNAMO_DB_TABLE')

# AWS clients
dynamo_db = boto3.client('dynamodb',region_name=reagion)

def authorization_required(func):
    def inner(request):
        # Check if the request has the authorization headers
        if "Authorization" not in request.headers:
            return JsonResponse({
                "error" : "'Authorization' header is required",
                "timestamp" : datetime.now().isoformat()
            },safe=False,status=400)
            
        # Auth token 
        authToken = request.headers["Authorization"]
            
        # Authorization is valid
        item = dynamo_db.get_item(
            TableName=dynamo_db_table,
            Key={
                "auth_token" : {
                    "S" : authToken
                }
            }
        )
        
        # Invalid auth token 
        if 'Item' not in item:
            return JsonResponse({
                "error" : "Invalid authorization token",
                "timestamp" : datetime.now().isoformat()
            },safe=False,status=401)
            
        # Check if the token has expired
        str_created = item["Item"]["created"]["S"]
        iso_created = datetime.fromisoformat(str_created)
        
        # Check expiry
        if iso_created + timedelta(hours=1) < datetime.now():
            return JsonResponse({
                "error" : "Authorization token has expired",
                "timestamp" : datetime.now().isoformat()
            },safe=False,status=403)
        
        # Attach the user to the request
        str_username = item["Item"]["username"]["S"]
        
        # Set the user 
        user = User.getUserByUsername(str_username)
        
        # Is user is null
        if not user:
            return JsonResponse({
                "error" : "An error occured while fetching your user",
                "timestamp" : datetime.now().isoformat()
            },safe=False,status=500)
            
        
        # Disabled user
        if user.active == False:
            return JsonResponse({
                "error" : "This user is disabled",
                "timestamp" : datetime.now().isoformat()
            },safe=False,status=403)
            
        request.user = user 
            
        return func(request)
    return inner


def json_required(keys={}):
    def decorator(func,keys=keys):
        def inner(request,keys=keys):
            # try and parse the request body
            try:
                json_body : Dict  = json.loads(request.body)
            except Exception as e:
                return JsonResponse({
                    'error' : 'Json is required as the request body'
                },safe=False,status=415)
            
            # check for the required keys
            missingKeys = [key for key in keys if key not in json_body]
            
            if missingKeys != []:
                return JsonResponse({
                    "error" : "Missing keys",
                    "keys" : missingKeys
                },safe=False,status=400)
            
            # Add the body to the request
            request.json_body = json_body
            
            return func(request)
        
        
        return inner
    return decorator

def requires_permissions(permissions=[]):
    def decorator(func,required_permissions=permissions):
        def inner(request, required_permissions=required_permissions):
            if not request.user:
                return JsonResponse({
                    "error" : "view configuration error",
                    "timestamp" : datetime.now().isoformat()
                },status=500)
                
            for permission in required_permissions:
                if not shared_models.Permission.has_permission(request.user,permission):
                    return JsonResponse({
                        "error" : f"User has missing permission '{permission}'",
                        "timestamp" : datetime.now().isoformat()
                    },status=403)
                    
            return func(request)
        return inner
    return decorator
                