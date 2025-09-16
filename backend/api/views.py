from django.http import JsonResponse
import os
from datetime import datetime, timedelta
from uuid import uuid4
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import boto3
import logging
from .decorators import authorization_required, json_required, requires_permissions, referenced_request
from . import models as api_models
from django.views.decorators.cache import cache_page
from shared_models import models as shared_models
from socket_io.helper import instance as socket_ioHelperInstance
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from utils.common import resizeAndRemoveBackground
from io import BytesIO
from .error_mappings import ErrorCode

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

@referenced_request("health")
def health(request):
    ref = request.ref
    return JsonResponse({
        "application" : os.getenv("APPLICATION_NAME"),
        "timestamp" : datetime.now().isoformat()
    },safe=False)

@csrf_exempt
@require_http_methods(["POST"])
@referenced_request("authenticate")
@json_required(keys={'username','password'})
def authenticate(request):
    # Request reference 
    ref = request.ref
    
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
@referenced_request("upload-file")
@authorization_required
@requires_permissions(['upload-file'])
def file_upload(request):
    # Request reference 
    ref = request.ref
    
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
        
        
    # Resize the image
    image = resizeAndRemoveBackground(file)
    
    # Upload to s3
    extension = file.name.split(".")[-1]
    filename = f'{ref}.{extension}'
    key = f"uploads/{filename}"
    
    try:
        inMemFile = BytesIO()
        image.save(inMemFile,format="png")
        inMemFile.seek(0)
        
        s3.upload_fileobj(inMemFile,FILE_S3_BUCKET,key)
    except Exception as e:
        logging.error(f'{ref} - Failed to upload file to s3 - {e}')
        return JsonResponse({
            'error' : 'Failed to upload file to s3 buckets',
            'ref' : ref,
            "timestamp" : datetime.now().isoformat()
        },status=500)
        
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
@referenced_request("get-products")
@authorization_required
def getProducts(request):
    # Request reference
    ref = request.ref
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
@referenced_request("get-product")
@authorization_required
def getProduct(request):
    # Ref 
    ref = request.ref
    
    # Check if reference is in request get 
    if 'reference' not in request.GET:
        return JsonResponse({
            "code" : ErrorCode.MISSING_ATTRIBUTE.value,
            "error" : "Key 'reference' was not found in request",
            "objects" : ['reference'],
            "timestamp" : datetime.now().isoformat(),
            "ref" : ref
        },status=400)
    
    # Get the product with the reference 
    productReference = request.GET['reference']
    product = shared_models.Product.getUsingRef(productReference)
    
    # If null return not found 
    if not product:
        return JsonResponse({
            "code" : ErrorCode.PRODUCT_NOT_FOUND.value,
            "error" : f"product with reference '{productReference}' was not found",
            "objects" : [productReference],
            "timestamp" : datetime.now().isoformat(),
            "ref" : ref
        },status=404)
        
    # Return the product 
    return JsonResponse({
        "product" : product.toDict(),
        "timestamp" : datetime.now().isoformat(),
        "ref" : ref
    })
        
@csrf_exempt
@require_http_methods(['GET'])
@referenced_request("get-categories")
@authorization_required
def getCategories(request):
    # Reference
    ref = request.ref
    
    # Category 
    categories = shared_models.ProductCategory.objects.all()
    
    # All products category 
    categoryAllProduct = {
        "id" : "all-category",
        "name" : "All",
        "ref" : "*",
        "stock_count" : shared_models.Product.objects.count(),
        "last_updated" : datetime.now().isoformat()
    }
    
    # In cart product category
    categoryInCart = {
        "id" : "cart",
        "name" : "In Cart",
        "ref" : "cart",
        "icon" : "shopping-basket.svg",
        "stock_count" : "My",
        "last_updated" : datetime.now().isoformat()
    }
    
    
    # Serialize categories 
    s_categories = [categoryAllProduct] + [category.toDict() for category in categories] + [categoryInCart]
    
    # Response 
    return JsonResponse({
        "ref" : ref,
        "count" : len(s_categories),
        "categories" : s_categories,
        "timestamp" : datetime.now().isoformat()
    })

@cache_page(60)
@csrf_exempt
@require_http_methods(['GET'])
@referenced_request("get-product-stock-filters")
@authorization_required
def getProductStockFilters(request):
    # Reference
    ref = request.ref
    
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
@referenced_request("create-product")
@json_required(keys={"reference","name","description","category","price_usd","price_zwg","reorder_point","image_upload","expiry_day_buffer"})
@authorization_required
@requires_permissions(['create-product'])
def createProduct(request):
    # Ref 
    ref = request.ref
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
@referenced_request("complete-cart")
@json_required(keys={'cart_items','currency','idempotence_key','payment_option','commited'})
@authorization_required
@requires_permissions(permissions=['commit-sale'])
def completeCart(request):
    # ref 
    ref = request.ref
    
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
    
    # Notify the sale
    try:
        # Ensure the connection 
        socket_ioHelperInstance.ensure_connection(timeout=1)
        
        socket_ioHelperInstance.client.emit('on-event',{
            "event" : "cart-completed",
            "payload" : {
                "ref" : ref,
                "timestamp" : datetime.now().isoformat(),
                "idempotence_key" : idempotence_key,
                "cart_count" : len(cart_items)
            },
            "timestamp" : datetime.now().isoformat()
        })
    except Exception as e:
            logging.error(f"Failed to send socket.io notification - {e}")
    
    # Response
    return JsonResponse({
        "ref" : ref,
        "timestamp" : datetime.now().isoformat(),
        "idempotence_key" : idempotence_key,
        "cart_count" : len(cart_items)
    })
    
@csrf_exempt
@require_http_methods(['GET'])
@referenced_request("get-employee-details")
@authorization_required
def getEmployeeDetails(request):
    ref = request.ref
    user : api_models.User = request.user
    
    return JsonResponse({
        "ref" : ref,
        "code" : ErrorCode.NONE.value,
        "employee" : user.toDict(),
        "timestamp" : datetime.now().isoformat()
    })


@csrf_exempt
@require_http_methods(['GET'])
@referenced_request("get-product-updates")
@authorization_required
def getProductUpdates(request):
    # Ref 
    ref = request.ref
    
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
        lastFetchedDateIso = timezone.make_aware(lastFetchedDateIso)
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


@csrf_exempt
@require_http_methods(['GET'])
@referenced_request("get-teller-sales")
@authorization_required
def getTellerSales(request):
    ref = request.ref
    
    # Check if period is defined 
    if 'period' not in request.GET:
        return JsonResponse({
            "ref" : ref,
            "error" : "Parameter 'period' is not defined in request",
            "timestamp" : datetime.now().isoformat()
        })
    
    # Today
    period = request.GET.get('period')
    fromDate = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
    
    # If the filter is 2 days then subtract 2 days
    # If a week then subtrack a week 
    # and month subtract a month
    if period == 'two-days':
        fromDate -= timedelta(days=1)
    elif period == 'week':
        fromDate -= timedelta(weeks=1)
    elif period == 'month':
        fromDate -= relativedelta(months=1)
    
    fromDate = timezone.make_aware(fromDate)
    
    # Also return the total daily sales 
    salesStats = shared_models.ProductSale.getTotalSales(request.user,fromDate)
    
    return JsonResponse({
        "ref" : ref,
        "carts" : shared_models.ProductSale.getTellerSales(request.user,fromDate),
        "sales" : salesStats,
        "timestamp" : datetime.now().isoformat()
    }) 
    

@csrf_exempt
@require_http_methods(['PUT'])
@referenced_request("update-product")
@json_required(keys={'name','description','price_usd','price_zwg','reorder_point','expiry_day_buffer','image_upload','category'})
@authorization_required
@requires_permissions(permissions=['update-product'])
def updateProduct(request):
    ref = request.ref
    
    # Product reference 
    productReference = request.GET.get('product_reference')
    
    # Check if reference is in request GET 
    if not productReference:
        return JsonResponse({
            'ref' : ref,
            'code' : ErrorCode.MISSING_ATTRIBUTE.value,
            'error' : "Attribute 'product_reference' is not in request GET",
            'objects' : ['product_reference'],
            'timestamp' : datetime.now().isoformat()
        })
        
    
    # Get the product  
    product = shared_models.Product.getUsingRef(productReference)
    
    # Store a copy of the before  
    productBefore = product.toDict()
    
    # Product does not exist 
    if not product:
        return JsonResponse({
            'ref' : ref,
            'code' : ErrorCode.PRODUCT_NOT_FOUND.value,
            'error' : f'Product with provided reference not found',
            'objects' : [productReference],
            'timestamp' : datetime.now().isoformat()
        },status=404)
    
    # Find foregn objects (category,image_uploaded)
    category = shared_models.ProductCategory.getUsingRef(request.json_body['category'])
    image_uploaded = shared_models.Upload.getUsingRef(request.json_body['image_upload'])
    
    # If any is null 
    if not category:
        return JsonResponse({
            'ref' : ref,
            'code' : ErrorCode.PRODUCT_CATEGORY_NOT_FOUND.value,
            'error' : 'Provided product category was not found',
            'objects' : [request.json_body['category']],
            'timestamp' : datetime.now().isoformat()
        },status=404)
        
    # Update the product
    product.name = request.json_body['name']
    product.category = category
    product.description = request.json_body['description']
    product.price_usd = request.json_body['price_usd']
    product.price_zwg = request.json_body['price_zwg']
    
    # Add an upload image if there was one uploaded
    if image_uploaded:
        product.image_uploaded = image_uploaded
        
    product.reorder_point = request.json_body['reorder_point']
    product.expiry_day_buffer = request.json_body['expiry_day_buffer']
    product.save()
    product.refresh_from_db()
        
    return JsonResponse({
        'ref' : ref,
        'product' : {
            'before' : productBefore,
            'after' : product.toDict()
        },
        'timestamp' : datetime.now().isoformat()
    })
    
@csrf_exempt
@require_http_methods(['POST'])
@referenced_request("add-stock")
@json_required(keys={'earlist_expiry_date','stock_count','product_reference','buying_price_usd_each','buying_price_zwg_each'})
@authorization_required
@requires_permissions(permissions=['add-stock'])
def addStock(request):
    # Get the params 
    earlistExpiryDate = request.json_body['earlist_expiry_date']
    stockCount = int(request.json_body['stock_count'])
    productReference =  request.json_body['product_reference']
    buyingPriceUSDEach = request.json_body['buying_price_usd_each']
    buyingPriceZWGEach = request.json_body['buying_price_zwg_each']
    
    # Parse the earliest expiry date 
    try:
        earlistExpiryDate = datetime.fromisoformat(earlistExpiryDate)
        earlistExpiryDate = timezone.make_aware(earlistExpiryDate)
    except:
        return JsonResponse({
            'ref' : request.ref,
            'code' : ErrorCode.BAD_DATE_FORMAT.value,
            'error' : "Invalid iso date format",
            'objects' : [earlistExpiryDate],
            'timestamp' : datetime.now().isoformat()    
        },status=400)
    
    # Check if the product is valid 
    product = shared_models.Product.getUsingRef(productReference)
    
    # If null then return 404 
    if not product:
        return JsonResponse({
            'ref' : request.ref,
            'code' : ErrorCode.PRODUCT_NOT_FOUND.value,
            'error' : 'Product with provide reference was not found',
            'objects' : [productReference],
            'timestamp' : datetime.now().isoformat()
        },status=404)
    
    # Add the stock
    try: 
        shared_models.Stock(
            product = product,
            expires = earlistExpiryDate,
            count = stockCount,
            user = request.user,
            buying_price_usd_each = buyingPriceUSDEach,
            buying_price_zwg_each = buyingPriceZWGEach
        ).save()
    except:
        return JsonResponse({
            'ref' : request.ref,
            'code' : ErrorCode.COMPLETE_SYSTEM_ERROR.value,
            'error' : 'Failed to save record to database',
            'objects' : [productReference],
            'timestamp' : datetime.now().isoformat()
        },status=500)
    
    # Refresh from db    
    product.refresh_from_db()
    
    # Return success 
    return JsonResponse({
        'ref' : request.ref,
        'code' : ErrorCode.NONE.value,
        'product' : product.toDict(),
        'timestamp' : datetime.now().isoformat()
    })
    