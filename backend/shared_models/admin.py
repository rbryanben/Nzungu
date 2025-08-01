from django.contrib import admin
from .models import *

admin.site.register(Upload)
admin.site.register(ProductCategory)
admin.site.register(ProductStockStatusFilter)
admin.site.register(Product)
admin.site.register(Permission)