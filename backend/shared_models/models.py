from django.db import models
from datetime import datetime
from uuid import uuid4
import os
from api import models as api_models
from django.db.models import Sum
from django.db.models import Q
from typing import List

class ReferencedObject(models.Model):
    id = models.AutoField(primary_key=True)
    ref = models.CharField(max_length=256,blank=True)
    
    def save(self,*args,**kwargs):
        if not self.ref:
            self.ref = str(uuid4())
        return super().save(*args,**kwargs)
    
    class Meta:
        abstract = True

class Upload(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256)
    ref = models.CharField(max_length=256,unique=True)
    url = models.CharField(max_length=512)
    last_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.ref
    
    @staticmethod
    def getUsingRef(ref : str) -> 'Upload':
        return Upload.objects.filter(ref=ref).first()

class ProductCategory(ReferencedObject):
    name = models.CharField(max_length=128)
    icon = models.CharField(max_length=32)
    last_updated = models.DateTimeField(auto_now=True)
    
    @property
    def stock_count(self):
        return -1
    
    def __str__(self):
        return self.name
    
    def toDict(self):
        return {
            "id" : self.id,
            "name" : self.name,
            "ref" : self.ref,
            "icon" : self.icon,
            "stock_count" : self.stock_count,
            "last_updated" : self.last_updated
        }
        
    @staticmethod
    def getUsingRef(ref : str) -> 'ProductCategory' :
        return ProductCategory.objects.filter(ref=ref).first()

class ProductStockStatusFilter(ReferencedObject):
    name = models.CharField(max_length=256)
    icon = models.CharField(max_length=32)
    theme = models.CharField(max_length=32)
    value = models.CharField(max_length=32)
    subtext = models.CharField(max_length=128)
    last_updated = models.DateTimeField(auto_now=True)
    
    @property
    def count(self):
        return -1
    
    def __str__(self):
        return self.name
    
    def toDict(self):
        return {
            "id" : self.id,
            "ref" : self.ref,
            "name" : self.name,
            "icon" : self.icon,
            "stock_count" : self.count,
            "last_updated" : self.last_updated.isoformat()
        }

class Product(ReferencedObject):
    name = models.CharField(max_length=128)
    category = models.ForeignKey(ProductCategory,on_delete=models.DO_NOTHING,null=True)
    description = models.CharField(max_length=128)
    price_usd = models.FloatField(default=0)
    price_zwg = models.FloatField(default=0)
    image_uploaded = models.ForeignKey(Upload,on_delete=models.DO_NOTHING,null=True)
    reorder_point = models.IntegerField(default=0)
    expiry_day_buffer = models.IntegerField(default=5)
    last_updated = models.DateTimeField(auto_now=True)

    @property
    def earliest_expiry_date(self):
        return -1
    
    @property
    def sold(self):
        return ProductSale.countSold(self.ref)
    
    @property
    def in_stock(self):
        return Stock.countStock(self) - self.sold
    
    @property
    def filter(self):
        return "implement-filter"
    
    @property
    def fetched(self):
        return datetime.now().isoformat()
    
    def __str__(self):
        return self.name
    
    def toDict(self):
        return {
            "id" : self.id,
            "ref" : self.ref,
            "fetched" : datetime.now().isoformat(),
            "name" : self.name,
            "category" : {
                "name" : self.category.name,
                "ref" : self.category.ref
            },
            "description" : self.description,
            "in_stock" : self.in_stock,
            "price_usd" : self.price_usd,
            "price_zwg" : self.price_zwg if self.price_zwg > 0 else float(os.getenv("EXG_USD_ZWG")) * self.price_usd,
            "sold" : self.sold,
            "last_upated" : self.last_updated.isoformat(),
            "image_url" : self.image_uploaded.url,
            "reorder_point" : self.reorder_point,
            "earliest_expiry_date" : self.earliest_expiry_date,
            "expiry_day_buffer" : self.expiry_day_buffer,
            "filter" : self.filter
        }
    
    @staticmethod
    def getUsingRef(ref : str):
        return Product.objects.filter(ref=ref).first()

    @staticmethod
    def getProductsUpdatedAfter(datetime_ : datetime) -> List['Product']:
        
        # Get the unique ids
        stock_products = Stock.objects.filter(updated__gt=datetime_).values_list('product__ref', flat=True)
        sold_products = ProductSale.objects.filter(last_updated__gt=datetime_).values_list('product', flat=True)
        
        # Get the products
        updated_products = Product.objects.filter(
            Q(last_updated__gt=datetime_) |
            Q(ref__in=stock_products) |
            Q(ref__in=sold_products)   
        ).distinct()
        
        return [product.toDict() for product in updated_products]
        
class Permission(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(api_models.User,on_delete=models.CASCADE)
    permission = models.CharField(max_length=64)
    last_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.permission}"
    
    @staticmethod
    def has_permission(user : api_models.User, permission : str) -> bool:
        return Permission.objects.filter(
            user=user,
            permission=permission
        ).exists()
        
        
class Stock(ReferencedObject):
    product = models.ForeignKey(Product,on_delete=models.DO_NOTHING,null=True)
    expires = models.DateField()
    count = models.IntegerField()
    user = models.ForeignKey(api_models.User,on_delete=models.DO_NOTHING,null=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{'_'.join(self.product.name.lower().split(' '))}-{self.updated}"
    
    @staticmethod
    def countStock(product: Product) -> int:
        result = Stock.objects.filter(product=product).aggregate(total=Sum('count'))
        return result['total'] or 0
        

class ProductSale(ReferencedObject):
    product = models.CharField(max_length=256)
    count = models.IntegerField()
    price_usd = models.FloatField()
    price_zwg = models.FloatField()
    fetched = models.DateTimeField()
    commited = models.DateTimeField()
    teller = models.ForeignKey(api_models.User,on_delete=models.DO_NOTHING,null=True)
    last_updated = models.DateTimeField(auto_now=True)
    cart = models.CharField(max_length=128,null=True)
    currency = models.CharField(max_length=16)
    payment_option = models.CharField(max_length=16)
    
    @property
    def product_name(self):
        product = Product.getUsingRef(ref=self.product)
        return product.name if product else 'deleted-product'
    
    @staticmethod
    def countSold(product_ref) -> int:
        result = ProductSale.objects.filter(product=product_ref).aggregate(total=Sum('count'))
        return result['total'] or 0
    
    
    def __str__(self):
        return f"{self.cart} : {self.product_name}"
