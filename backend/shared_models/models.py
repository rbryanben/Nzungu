from django.db import models
from datetime import datetime
from uuid import uuid4
import os
import logging
from django.db.models import Sum, QuerySet, F
from django.db.models import Q
from typing import List, Dict
from socket_io.helper import instance as socket_ioHelperInstance
from django.utils import timezone
from datetime import timedelta
from django.core.cache import cache


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
    icon = models.CharField(max_length=32,null=True,blank=True)
    last_updated = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        
        # Notify that a new product category has been added
        try:
            # Ensure the connection 
            socket_ioHelperInstance.ensure_connection(timeout=1)
        
            socket_ioHelperInstance.client.emit('on-event',{
                "event" : "product-category-updated",
                "payload" : self.toDict(small=True),
                "timestamp" : datetime.now().isoformat()
            })
        except Exception as e:
            logging.error(f"Failed to send socket.io notification - {e}")
        
        return super().save(*args, **kwargs)
    
    @property
    def stock_count(self):
        return Product.objects.filter(category=self).count()
    
    def __str__(self):
        return self.name
    
    def toDict(self,small=False):
        if small:
            return {
                "id" : self.id,
                "name" : self.name,
                "ref" : self.ref
            }
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
    
    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)
    
    @property
    def count(self):
        # Cache
        cache_key = f'product-stock-filter-{self.ref}'
        cache_value = cache.get(cache_key)
        
        # Return the cached value
        if cache_value:
            return cache_value
        
        # Count the products
        result = len([product for product in Product.objects.all() if product.filter == self.value])
        cache.set(cache_key,result,300)
        
        return result
    
    def __str__(self):
        return self.name
    
    def toDict(self):
        return {
            "id" : self.id,
            "ref" : self.ref,
            "name" : self.name,
            "value" : self.value,
            "subtext" : self.subtext,
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

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        res = super().save(*args, **kwargs)

        event_name = "product-added" if is_new else "product-updated"
        
        try:
            # Ensure the connection 
            socket_ioHelperInstance.ensure_connection(timeout=1)
        
            socket_ioHelperInstance.client.emit('on-event', {
                "event": event_name,
                "payload": self.toDict(small=True),
                "timestamp": datetime.now().isoformat()
            })
            
        except Exception as e:
            logging.error(f"Failed to send socket.io notification - {e}")
            
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
        # Cache key 
        cache_key = f"product_filter_{self.pk}"
        cached_value = cache.get(cache_key)
        
        # Return the cached value
        if cached_value is not None:
            return cached_value
        
        # Out of stock then return 
        if self.in_stock <= 0:
            return 'out-of-stock'
        
        # Get stocks 
        stocksOrderedByExpiry = Stock.objects.filter(product=self).order_by("expires")
        
        # Sales 
        productSales = self.sold
        
        # Calculate
        totalStock = 0 
        earliestExpiryDate = None
        
        for stock in stocksOrderedByExpiry:
            totalStock += stock.count
            if totalStock > productSales:
                earliestExpiryDate = stock.expires
    
        # Expired
        now = timezone.now().date()
        if now >= earliestExpiryDate:
            result = "expired"
        
        # Almost expired
        elif earliestExpiryDate <= now + timedelta(days=self.expiry_day_buffer):
            result = 'almost-expired'
        
        # Low stock
        elif self.in_stock <= self.reorder_point:
            result = 'low-stock'
        
        else:    
            result = "in-stock"
    
        # ✅ store in cache for 3 minutes
        cache.set(cache_key, result, timeout=180)
        return result
    
    @property
    def fetched(self):
        return datetime.now().isoformat()
    
    
    def __str__(self):
        return self.name
    
    def toDict(self,small=False):
        
        if small:
            return {
                "fetched" : datetime.now().isoformat(),
                "name" : self.name,
                "category" : {
                    "name" : self.category.name,
                    "ref" : self.category.ref
                },
                "description" : self.description,
                "price_usd" : self.price_usd,
                "price_zwg" : self.price_zwg if self.price_zwg > 0 else float(os.getenv("EXG_USD_ZWG")) * self.price_usd,
                "image_url" : self.image_uploaded.url,
                "reorder_point" : self.reorder_point
            }
            
        res = {
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
            "last_upated" : self.last_updated.isoformat() if self.last_updated else  datetime.now().isoformat(),
            "image_url" : self.image_uploaded.url,
            "reorder_point" : self.reorder_point,
            "earliest_expiry_date" : self.earliest_expiry_date,
            "expiry_day_buffer" : self.expiry_day_buffer,
            "filter" : self.filter
        }
        
        return res
    
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
        
        return { product.ref:product.toDict() for product in updated_products}
        
class Permission(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey("api.User",on_delete=models.CASCADE)
    permission = models.CharField(max_length=64)
    last_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.permission}"
    
    @staticmethod
    def has_permission(user : "api.User", permission : str) -> bool:
        return Permission.objects.filter(
            user=user,
            permission=permission
        ).exists()
        
        
class Stock(ReferencedObject):
    product = models.ForeignKey(Product,on_delete=models.DO_NOTHING,null=True)
    expires = models.DateField()
    count = models.IntegerField()
    user = models.ForeignKey("api.User",on_delete=models.DO_NOTHING,null=True)
    updated = models.DateTimeField(auto_now=True)
    buying_price_usd_each = models.FloatField(default=0)
    buying_price_zwg_each = models.FloatField(default=0)

    def save(self, *args, **kwargs):
        try:
            # Ensure the connection 
            socket_ioHelperInstance.ensure_connection(timeout=1)
        
            # Notify that a new product category has been added
            socket_ioHelperInstance.client.emit('on-event',{
                "event" : "product-stock-updated",
                "payload" : self.toDict(),
                "timestamp" : datetime.now().isoformat()
            })
        except Exception as e:
            logging.error("Failed to emit 'product-stock-updated' event to socket.io - {e}")
            
        return super().save(*args, **kwargs)
    
    def toDict(self):
        return {
            "product" : self.product.toDict(),
            "expires" : self.expires.isoformat(),
            "count" : self.count,
            "updated" : self.updated.isoformat() if self.updated else datetime.now().isoformat()
        }
        
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
    teller = models.ForeignKey("api.User",on_delete=models.DO_NOTHING,null=True)
    last_updated = models.DateTimeField(auto_now=True)
    cart = models.CharField(max_length=128,null=True)
    currency = models.CharField(max_length=16)
    payment_option = models.CharField(max_length=16)
    
    def toDict(self):
        product = Product.objects.select_related("image_uploaded","category").get(ref=self.product)
        return { 
            "id": product.id, 
            "ref": product.ref,
            "fetched": self.fetched,
            "name": product.name, 
            "category": product.category.toDict(), 
            "description": product.description,
            "in_stock": product.in_stock,
            "price_usd": self.price_usd,
            "price_zwg": self.price_zwg,
            "sold": product.sold,
            "last_upated": product.last_updated,
            "image_url": product.image_uploaded.url, 
            "reorder_point": product.reorder_point, 
            "earliest_expiry_date": -1, 
            "expiry_day_buffer": product.expiry_day_buffer, 
            "filter": product.filter,
            "count" : 1
        }
        
    @property
    def product_name(self):
        product = Product.getUsingRef(ref=self.product)
        return product.name if product else 'deleted-product'
    
    @staticmethod
    def countSold(product_ref) -> int:
        result = ProductSale.objects.filter(product=product_ref).aggregate(total=Sum('count'))
        return result['total'] or 0
    
    @staticmethod
    def getSalesFromCart(cart : str) -> QuerySet['ProductSale']:
        return ProductSale.objects.filter(cart=cart)
    
    @staticmethod
    def getTotalSales(user, fromDate):
        # Cash sales USD
        totalSalesCashUSD = ProductSale.objects.filter(
            currency="USD",
            teller=user,
            payment_option="cash",
            commited__gt=fromDate
        ).aggregate(
            total=Sum(F("count") * F("price_usd"))
        )["total"] or 0

        # Cash sales ZWG
        totalSalesCashZWG = ProductSale.objects.filter(
            currency="ZWG",
            teller=user,
            payment_option="cash",
            commited__gt=fromDate
        ).aggregate(
            total=Sum(F("count") * F("price_zwg"))
        )["total"] or 0

        # Non-cash (anything not cash) USD
        totalSalesNonCashUSD = ProductSale.objects.filter(
            currency="USD",
            teller=user,
            commited__gt=fromDate
        ).exclude(payment_option="cash").aggregate(
            total=Sum(F("count") * F("price_usd"))
        )["total"] or 0

        # Non-cash (anything not cash) ZWG
        totalSalesNonCashZWG = ProductSale.objects.filter(
            currency="ZWG",
            teller=user,
            commited__gt=fromDate
        ).exclude(payment_option="cash").aggregate(
            total=Sum(F("count") * F("price_zwg"))
        )["total"] or 0

        return {
            "cash_usd": {
                "total": totalSalesCashUSD,
                "total_yesterday": totalSalesCashUSD,  # TODO: replace with real yesterday query
            },
            "cash_zwg": {
                "total": totalSalesCashZWG,
                "total_yesterday": totalSalesCashZWG,
            },
            "bank_usd": {  # really means non-cash
                "total": totalSalesNonCashUSD,
                "total_yesterday": totalSalesNonCashUSD,
            },
            "bank_zwg": {  # really means non-cash
                "total": totalSalesNonCashZWG,
                "total_yesterday": totalSalesNonCashZWG,
            },
        }
        
    
    @staticmethod
    def getTellerSales(teller : "api.User", fromDate : datetime) -> List[Dict]:
        
        # All sales frm the given date 
        carts = ProductSale.objects.filter(
            teller=teller,
            last_updated__gt=fromDate
        ).values_list('cart',flat=True).distinct().order_by("commited")
        
        # Grouped sales 
        groupedSales = []
        
        # Iterate the carts
        for cart in carts:
            # Get the sales 
            sales = ProductSale.getSalesFromCart(cart)
            
            # Products grouped 
            products = {}
            
            # Iterate the sales
            for sale in sales:
                # If sale in product
                if sale.product in products:
                    products[sale.product]['count'] += 1 
                    continue    
                
                # If sale not in products then add it with a count of 1
                productSaleDict = sale.toDict()
                productSaleDict['count'] = 1
                products[sale.product] = productSaleDict
                
                
            # Add to grouped sales 
            groupedSales.append({
                "timestamp": sales[0].commited,
                "ref": cart,
                "payment_method": sales[0].payment_option,
                "currency": sales[0].currency,
                "items" : [products[productName] for productName in products.keys()]
            })
        
        
        return groupedSales
    
    def __str__(self):
        return f"{self.cart} : {self.product_name}"
