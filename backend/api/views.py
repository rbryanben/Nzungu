from django.http import JsonResponse
import os
from datetime import datetime
from uuid import uuid4
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import boto3
import logging
from .decorators import authorization_required, json_required, requires_permissions
from . import models as api_models
from shared_models import models as shared_models

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
    user = api_models.User.getUserByUsername(username)
    
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
@requires_permissions(['upload-file'])
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
    file_url = f"https://{FILE_S3_BUCKET}.s3.{AWS_REAGION}.amazonaws.com/{key}"
    
    # Store the file object
    shared_models.Upload(
        name = filename,
        ref = ref,
        url = file_url
    ).save()
        
    return JsonResponse({
        "filename" : filename,
        "url" : file_url,
        "ref" : ref,
        "timestamp" : datetime.now().isoformat()
    })
    
    
@csrf_exempt
@require_http_methods(['GET'])
@authorization_required
def getProducts(request):
    # Request reference
    ref = str(uuid4())
    request_time = datetime.now().isoformat()
    
    
    # Products 
    products = shared_models.Product.objects.select_related(
            'category',
            'image_uploaded'
        ).order_by('-id')
    
    # Serialize
    s_products = [product.toDict() for product in products]
    
    # Return the response 
    return JsonResponse({
        "ref" : ref,
        "count" : len(s_products),
        "products" : s_products,
        "timestamp" : request_time
    }) 
    
@csrf_exempt
@require_http_methods(['GET'])
@authorization_required
def getCategories(request):
    # Reference
    ref = str(uuid4())
    
    # Category 
    categories = shared_models.ProductCategory.objects.all()
    
    # Serialize categories 
    s_categories = [category.toDict() for category in categories]
    
    # Response 
    return JsonResponse({
        "ref" : ref,
        "count" : len(s_categories),
        "categories" : s_categories,
        "timestamp" : datetime.now().isoformat()
    })

@csrf_exempt
@require_http_methods(['GET'])
@authorization_required
def getProductStockFilters(request):
    # Reference
    ref = str(uuid4())
    
    # Filter 
    filters = shared_models.ProductStockStatusFilter.objects.all()
    
    # Serialize filters 
    s_filters = [filter.toDict() for filter in filters]
    
    # Response 
    return JsonResponse({
        "ref" : ref,
        "count" : len(s_filters),
        "filters" : s_filters,
        "timestamp" : datetime.now().isoformat()
    })
    
@csrf_exempt
@require_http_methods(["POST"])
@json_required(keys={"reference","name","description","category","price_usd","price_zwg","reorder_point","image_upload","expiry_day_buffer"})
@authorization_required
@requires_permissions(['create-product'])
def createProduct(request):
    # Ref 
    ref = str(uuid4())
    json_body = request.json_body
    request_time = datetime.now().isoformat()
    
    # Get the category 
    category = shared_models.ProductCategory.getUsingRef(json_body['category'])
    image_uploaded = shared_models.Upload.getUsingRef(json_body['image_upload'])
    
    # check category
    if not category:
        return JsonResponse({
            "error" : "category with the given reference was not found",
            "timestamp" : datetime.now().isoformat(),
            "ref" : ref
        },status=400)
    
    # image upload
    if not image_uploaded:
        return JsonResponse({
            "error" : "image_upload with the given reference was not found",
            "timestamp" : datetime.now().isoformat(),
            "ref" : ref
        },status=400)
        
    
    # Create the product
    product = shared_models.Product(
        name = json_body['name'],
        category = category,
        description = json_body['description'],
        price_usd = float(json_body['price_usd']),
        price_zwg = float(json_body['price_zwg']),
        image_uploaded = image_uploaded,
        reorder_point = float(json_body['reorder_point']),
        expiry_day_buffer = int(json_body['expiry_day_buffer'])
    )
    
    # Save the product
    product.save()
    
    # Response
    return JsonResponse({
        "ref" : product.ref,
        "product" : product.toDict(),
        "timestamp" : request_time
    }) 
    
@csrf_exempt
@require_http_methods(['POST'])
@json_required(keys={'cart_items','currency','idempotence_key','payment_option','commited'})
@authorization_required
@requires_permissions(permissions=['commit-sale'])
def completeCart(request):
    # ref 
    ref = str(uuid4())
    
    # Json body
    json_body = request.json_body
    
    # Parameters 
    cart_items = json_body['cart_items']
    currency = json_body['currency']
    idempotence_key = json_body['idempotence_key']
    payment_option = json_body['payment_option']
    commited = json_body['commited']
    
    # Iterate through the cart and create the related object
    cart_sales = [] 
    for item in cart_items:
        cart_sales.append(
            shared_models.ProductSale(
                product = item['ref'],
                count = 1,
                price_usd = item['price_usd'],
                price_zwg = item['price_zwg'],
                fetched = item['fetched'],
                teller = request.user,
                cart = idempotence_key,
                currency = currency,
                commited = commited,
                payment_option = payment_option
            )
        )
        
    # Bulk save 
    shared_models.ProductSale.objects.bulk_create(cart_sales)
        
    return JsonResponse({
        "ref" : ref,
        "timestamp" : datetime.now().isoformat(),
        "idempotence_key" : idempotence_key,
        "cart_count" : len(cart_items)
    })
    
@csrf_exempt
@require_http_methods(['GET'])
@authorization_required
def getProductUpdates(request):
    # Ref 
    ref = str(uuid4())
    
    # Check for the required keys 
    if 'last-fetched-date-iso' not in request.GET:
        return JsonResponse({
            "ref" : ref,
            "error" : "key 'last-fetched-date-iso' is required in GET parameters",
            "timestamp" : datetime.now().isoformat()
        },status=400)
    
    # Parse the iso date 
    try:
        lastFetchedDateIso = datetime.fromisoformat(request.GET['last-fetched-date-iso'])
    except:
        return JsonResponse({
            "ref" : ref,
            "error" : "Bad 'last-fetched-date-iso' attribute",
            "timestamp" : datetime.now().isoformat()
        },status=400)
        
    # Fetch any product that was updated after the given iso time stamp
    products = shared_models.Product.getProductsUpdatedAfter(lastFetchedDateIso)
    
    # Return the products 
    return JsonResponse({
        'ref' : ref,
        'products' : products,
        'count' : len(products),
        'timestamp' : datetime.now().isoformat()
    },safe=False)
